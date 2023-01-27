#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   check_schema.py
"""

import os
import json
import argparse
import collections
import jsonschema
import urllib
import yaml
import codecs
import re

from logging import getLogger, StreamHandler, DEBUG

logger = getLogger(__name__)

handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class Error(BaseException):
    """
    エラークラス
    """

    def __init__(self, message, flag_print=True):
        self.__message = message

        if flag_print:
            logger.error(" ==> Error()")
            logger.error("     message = {}".format(self.__message))

    def message(self):
        return self.__message


def load_yaml(filename):
    """
    utility function (YAML読み込み)
    """
    yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                         lambda loader, node: collections.OrderedDict(loader.construct_pairs(node)))

    loader = yaml.SafeLoader
    # lodaerを編集 (指数表記をfloatと柔軟に認識させるため)
    # Ref.: https://stackoverflow.com/questions/30458977/yaml-loads-5e-6-as-string-and-not-a-number
    loader.add_implicit_resolver(
        u'tag:yaml.org,2002:float',
        re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
        list(u'-+0123456789.'))

    vdict = collections.OrderedDict()
    with codecs.open(filename, "r", "utf-8") as f:
        vdict = yaml.load(f, Loader=loader)
    return vdict


def load_json(filename):
    """
    utiltiy function (json読み込み)
    """

    ret_dict = collections.OrderedDict()
    with codecs.open(filename, "r", "utf-8") as f:
        ret_dict = json.load(f, object_pairs_hook=collections.OrderedDict)
    return ret_dict


def check_schema(metadata_filename, schema_path):
    """
    メタデータのスキーマチェック

    Args:
        metadata_filename (str): メタデータ管理エクセルファイルパス
        schema_path (str): jsonshemaのパス (ファイル名 or URL)
    """

    def is_url(text):
        url_param = urllib.parse.urlparse(text)
        return len(url_param.scheme) > 0

    schema = dict()
    if is_url(schema_path):
        try:
            with urllib.request.urlopen(schema_path) as f:
                schema = json.load(f)
        except urllib.error.URLError as e:
            raise Error(e)
    else:
        with open(schema_path, encoding="utf-8") as f:
            schema = json.load(f)

    logger.info("... get schema from {}".format(schema_path))

    error_dict = collections.OrderedDict()
    error_dict["error"] = "Invalid metadata schema"
    error_dict["details"] = collections.OrderedDict()

    for metadata_file in [metadata_filename]:

        # ... validation check
        schema_used = schema

        ext_without_dot = os.path.splitext(metadata_file)[1][1:].lower()
        obj = None
        if ext_without_dot in ["json"]:
            obj = load_json(metadata_file)
        elif ext_without_dot in ["yaml", "yml"]:
            obj = load_yaml(metadata_file)
        else:
            raise Exception(f'Invalid format for {metadata_file}')

        validator = jsonschema.Draft202012Validator(schema_used)
        validation_errors = sorted(
            validator.iter_errors(obj), key=lambda e: e.path)

        errors = []

        for error in validation_errors:
            message = error.message
            if error.path:
                message = "[{}] {}".format(
                    ".".join(str(x) for x in error.absolute_path), message
                )
                errors.append(message)

        status = "OK"
        if len(errors) > 0:
            status = "NG"
            error_dict["details"][metadata_file] = errors

        logger.info("... check {}: {}".format(metadata_file, status))

    error_list = list(error_dict["details"].keys())
    if len(error_list) > 0:
        message = json.dumps(error_dict, indent=4)
        Error(message)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='check chema for metadata with yaml')
    parser.add_argument('metadata_filename',
                        help='metadata filename for yaml/json')

    args = parser.parse_args()
    metadata_filename = args.metadata_filename

    config_dict = load_yaml("config.yml")
    schema_path = config_dict.get("schema_path", "./schema/schema.json")

    logger.info("... input metadata: {}".format(metadata_filename))
    logger.info("... schema path: {}".format(schema_path))

    check_schema(metadata_filename, schema_path)
