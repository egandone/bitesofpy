import configparser
import re

class ToxIniParser:
    def __init__(self, ini_file):
        """Use configparser to load ini_file into self.config"""
        self._config = configparser.ConfigParser()
        self._config.read(ini_file)

    @property
    def number_of_sections(self):
        """Return the number of sections in the ini file.
           New to properties? -> https://pybit.es/property-decorator.html
        """
        return len(self._config.sections())

    @property
    def environments(self):
        """Return a list of environments
           (= "envlist" attribute of [tox] section)"""
        return [env.strip() for env in re.split(',|\n', self._config['tox']['envlist']) if env.strip()]

    @property
    def base_python_versions(self):
        """Return a list of all basepython across the ini file"""
        all_bases = set()
        for section in self._config.sections():
            if 'basepython' in self._config[section]:
                all_bases.add(self._config[section]['basepython'])
        return all_bases