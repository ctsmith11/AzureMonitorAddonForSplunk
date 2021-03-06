# encoding = utf-8
'''
#
# AzureMonitorAddonForSplunk
#
# Copyright (c) Microsoft Corporation
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
'''
import argparse
import splunklib.client as client

MASK = '********'

def mask_password(name, session_key):
    '''
        modify contents of launcher's inputs.conf
    '''
    try:
        token = {'token': session_key}
        service = client.connect(**token)
        kind, input_name = name.split("://")
        item = service.inputs.__getitem__((input_name, kind))

        kwargs = {
            'vaultName': item.content.vaultName,
            'SPNTenantID': item.content.SPNTenantID,
            'SPNApplicationId': MASK,
            'SPNApplicationKey': MASK,
            'eventHubNamespace': item.content.eventHubNamespace,
            'secretName': item.content.secretName,
            'secretVersion': item.content.secretVersion,
            'index': item.content.index,
            'interval': item.content.interval,
            'sourcetype': item.content.sourcetype
        }

        item.update(**kwargs).refresh()

    except Exception as e:
        print "azure_diagnostic_logs: Error updating inputs.conf: %s" % str(e)

def main():
    '''
        parse arguments and call the required function
    '''
    parser = argparse.ArgumentParser(description='modify values in inputs.conf')
    parser.add_argument('-n', type=str, required=True, dest='data_input_name')
    parser.add_argument('-k', type=str, required=True, dest='session_key')
    args = parser.parse_args()

    mask_password(args.data_input_name, args.session_key)

if __name__ == "__main__":
    main()
