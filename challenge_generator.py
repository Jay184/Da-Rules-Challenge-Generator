"""
Create custom challenges for "The Binding of Isaac" from the Mod "Da Rules".
"""

from typing import Optional


def create(steam_path: str,
           challenge_name: str,
           description: Optional[str] = None,
           directory_name: Optional[str] = None) -> None:
    """
    Creates a custom challenge directory in the "mods" folder of the game.
    @param steam_path: The directory where the game is located.
            E.g. "C:\Steam\steamapps\common\The Binding of Isaac Rebirth"
    @param challenge_name: The name as it should appear in the game.
    @param description: A description of the challenge.
    @param directory_name: A custom directory name, if left empty the challenge name will be used.
    @return: None
    """
    import os

    # Template strings
    template_metadata = '''<?xml version="1.0" encoding="UTF-8"?>
<metadata>
    <name>{name}</name>
    <directory>{directory}</directory>
    <id>848225254</id>
    <description>{description}</description>
    <version>1.1</version>
    <visibility>Public</visibility>
    <tag id="Challenges"/>
</metadata>
'''

    template_main = '''local challengename = "{name}"
local moddata = "[data]{data}[/data]"
local mod = RegisterMod(challengename, 1)
local challengeid = Isaac.GetChallengeIdByName(challengename)

if not DRChallengesData then
  DRChallengesData = {{}}
end
DRChallengesData[challengeid] = moddata
'''

    template_challenges = '''<challenges version="1">
<challenge name="{name}" endstage="12" altpath="false" />
</challenges>
'''

    isaac_path = os.path.join(steam_path, r'The Binding of Isaac Rebirth')
    mods_path = os.path.join(isaac_path, r'mods')

    # Read rules
    data_file_path = os.path.join(isaac_path, r'data\da rules\save1.dat')
    data_file = open(data_file_path, 'r')

    data = None
    for line in data_file:
        # The string is not required to be in the same line.
        # But we ignore this for now because the game/mod will always generate it in one line
        if '[data]' in line and '[/data]' in line:
            data = line.split('[data]')[1]
            data = data.split('[/data]')[0]
    data_file.close()

    if not data:
        raise Exception(f'Could not get data from "{data_file_path}".')

    description = description or 'No description given.'
    directory_name = directory_name or '_'.join(directory_name.split(' '))

    # Create challenge directories
    challenge_path = os.path.join(mods_path, directory_name)
    challenge_content_path = os.path.join(challenge_path, 'content')

    try:
        os.mkdir(challenge_path)
        os.mkdir(challenge_content_path)
    except FileExistsError:
        pass

    # Write the files
    metadata_file = open(os.path.join(challenge_path, 'metadata.xml'), 'w')
    metadata_file.write(
        template_metadata.format(name=challenge_name, directory=directory_name, description=description))
    metadata_file.close()

    main_file = open(os.path.join(challenge_path, 'main.lua'), 'w')
    main_file.write(template_main.format(name=challenge_name, data=data))
    main_file.close()

    challenges_file = open(os.path.join(challenge_content_path, 'challenges.xml'), 'w')
    challenges_file.write(template_challenges.format(name=challenge_name))
    challenges_file.close()

    print('Done.')


if __name__ == '__main__':
    import sys

    args = sys.argv[1:]

    if not args or len(args) < 2:
        print(f'Usage: {__file__} (STEAMDIR) (NAME) [DESCRIPTION] [DIRECTORYNAME]')
        sys.exit(1)

    args2 = args[2] if len(args) >= 2 else None
    args3 = args[3] if len(args) >= 3 else None
    create(args[0], args[1], args2, args3)
