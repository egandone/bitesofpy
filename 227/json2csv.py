from pathlib import Path
import csv
import json
from json.decoder import JSONDecodeError

EXCEPTION = 'exception caught'
TMP = Path('/tmp')


def convert_to_csv(json_file):
    """Read/load the json_file (local file downloaded to /tmp) and
        convert/write it to defined csv_file.
         The data is in mounts > collected

        Catch bad JSON (JSONDecodeError) file content, in that case print the defined
        EXCEPTION string ('exception caught') to stdout reraising the exception.
        This is to make sure you actually caught this exception.

        Example csv output:
        creatureId,icon,isAquatic,isFlying,isGround,isJumping,itemId,name,qualityId,spellId
        32158,ability_mount_drake_blue,False,True,True,False,44178,Albino Drake,4,60025
        63502,ability_mount_hordescorpionamber,True,...
        ...
    """  # noqa E501
    csv_file = TMP / json_file.name.replace('.json', '.csv')

    try:
        with open(json_file) as json_in:
            parsed_json = json.loads(json_in.read())

        keys = parsed_json['mounts']['collected'][0].keys()
        with open(csv_file, 'w') as csv_out:
            csv_out.write(','.join(keys) + '\n')
            for collected in parsed_json['mounts']['collected']:
                values = []
                for key in keys:
                    values.append(str(collected[key]))
                bytes_written = csv_out.write(','.join(values) + '\n')
    except JSONDecodeError as jsonde:
        print(EXCEPTION)
        raise jsonde
