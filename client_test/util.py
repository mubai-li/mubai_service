# from requests.utils import (
#
#     guess_filename,
#     to_key_val_list,
# )
from typing import Mapping
import os
from urllib3.fields import RequestField
from urllib3.filepost import encode_multipart_formdata


def guess_filename(obj):
    """Tries to guess the filename of the given object."""
    name = getattr(obj, "name", None)
    if name and isinstance(name, basestring) and name[0] != "<" and name[-1] != ">":
        return os.path.basename(name)


def to_key_val_list(value):
    if value is None:
        return None

    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError("cannot encode objects that are not 2-tuples")

    if isinstance(value, Mapping):
        value = value.items()

    return list(value)


basestring = (str, bytes)


def _encode_files(files, data):
    """Build the body for a multipart/form-data request.

    Will successfully encode files when passed as a dict or a list of
    tuples. Order is retained if data is a list of tuples but arbitrary
    if parameters are supplied as a dict.
    The tuples may be 2-tuples (filename, fileobj), 3-tuples (filename, fileobj, contentype)
    or 4-tuples (filename, fileobj, contentype, custom_headers).
    """
    if not files:
        raise ValueError("Files must be provided.")
    elif isinstance(data, basestring):
        raise ValueError("Data must not be a string.")

    new_fields = []
    fields = to_key_val_list(data or {})
    files = to_key_val_list(files or {})

    for field, val in fields:
        if isinstance(val, basestring) or not hasattr(val, "__iter__"):
            val = [val]
        for v in val:
            if v is not None:
                # Don't call str() on bytestrings: in Py3 it all goes wrong.
                if not isinstance(v, bytes):
                    v = str(v)

                new_fields.append(
                    (
                        field.decode("utf-8")
                        if isinstance(field, bytes)
                        else field,
                        v.encode("utf-8") if isinstance(v, str) else v,
                    )
                )

    for k, v in files:
        # support for explicit filename
        ft = None
        fh = None
        if isinstance(v, (tuple, list)):
            if len(v) == 2:
                fn, fp = v
            elif len(v) == 3:
                fn, fp, ft = v
            else:
                fn, fp, ft, fh = v
        else:
            fn = guess_filename(v) or k
            fp = v

        if isinstance(fp, (str, bytes, bytearray)):
            fdata = fp
        elif hasattr(fp, "read"):
            fdata = fp.read()
        elif fp is None:
            continue
        else:
            fdata = fp

        rf = RequestField(name=k, data=fdata, filename=fn, headers=fh)
        rf.make_multipart(content_type=ft)
        new_fields.append(rf)

    body, content_type = encode_multipart_formdata(new_fields)

    return body, content_type


