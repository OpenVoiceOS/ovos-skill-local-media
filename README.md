# <img src='https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/folder-open.svg' card_color='#55dffe' width='50' height='50' style='vertical-align:bottom'/> File Browser

![ocp_file_browser](https://github.com/OpenVoiceOS/ovos-skill-local-media/assets/33701864/d88630f2-3291-410a-a499-1d33ab93415c)

## About

This is a file browser skill for OpenVoice OS. It builds a local index of your
media files so you can find them by voice.

Organize your media collection like this so the skill can find it:

    ~/OCPMedia/Music
    ~/OCPMedia/Movies
    ~/OCPMedia/Podcasts
    ~/OCPMedia/...

The skill maps each top-level folder to a media type. It loads each subfolder
as a playlist.

You can set the base folder in the skill settings. The default is
`~/OCPMedia`.

```json
{
  "media_path": "~/OCPMedia"
}
```

## Install

Install this skill through the OVOS skill installer, or add it to your OVOS
instance as any other `ovos.plugin.skill` entry point.

## Examples

* "Open File Browser"
* "Show File Browser"

## Related projects

* [OpenVoiceOS/ovos-shell](https://github.com/OpenVoiceOS/ovos-shell) — the QML shell this skill's GUI needs.
* [OpenVoiceOS/ovos-core](https://github.com/OpenVoiceOS/ovos-core) — the OVOS assistant core that loads this skill.

## Credits

Aditya Mehra (@AIIX)

## Category

**Daily**

## Tags

#filebrowser
#browser
#file
#manager
#local
#usb

## Notes

* This skill needs the latest [OVOS Shell](https://github.com/OpenVoiceOS/ovos-shell).
* This skill is not backward compatible with the Mycroft-Core GUI API. It needs the OVOS QML plugin from ovos-shell.

## License

See [LICENSE](LICENSE).
