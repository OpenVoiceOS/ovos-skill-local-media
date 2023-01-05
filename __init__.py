#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2022 by Aditya Mehra <Aix.m@outlook.com>
# All rights reserved.

import os
import subprocess
from mycroft.skills.core import MycroftSkill, intent_file_handler
from ovos_plugin_common_play.ocp.status import *
from mycroft_bus_client.message import Message

__author__ = 'aix'


class FileBrowserSkill(MycroftSkill):
    def __init__(self):
        """
        FileBrowserSkill Skill Class.
        """
        super(FileBrowserSkill, self).__init__(name="FileBrowserSkill")
        self.skill_location_path = None
        self.udev_thread = None

    def initialize(self):
        self.add_event('skill.file-browser.openvoiceos.home', self.show_home)
        self.gui.register_handler('skill.file-browser.openvoiceos.handle.file', self.handle_file)
        self.gui.register_handler('skill.file-browser.openvoiceos.handle.folder.playlists', self.handle_folder_playlist)
        self.gui.register_handler('skill.file-browser.openvoiceos.send.file.kdeconnect', self.share_to_device_kdeconnect)
        self.audioExtensions = ["aac", "ac3", "aiff", "amr", "ape", "au", "flac", "alac" , "m4a", "m4b", "m4p", "mid", "mp2", "mp3", "mpc", "oga", "ogg", "opus", "ra", "wav", "wma"]
        self.videoExtensions = ["3g2", "3gp", "3gpp", "asf", "avi", "flv", "m2ts", "mkv", "mov", "mp4", "mpeg", "mpg", "mts", "ogm", "ogv", "qt", "rm", "vob", "webm", "wmv"]
        self.skill_location_path = os.path.dirname(os.path.realpath(__file__))
        self.setup_udev_monitor()

    def setup_udev_monitor(self):
        try:
            import pyudev
            # We want to monitor for USB devices being added or removed
            context = pyudev.Context()
            monitor = pyudev.Monitor.from_netlink(context)
            monitor.filter_by(subsystem='usb')
            # Start monitoring in a separate thread
            self.udev_thread = pyudev.MonitorObserver(monitor, self.handle_udev_event)
            self.udev_thread.start()
    
        except Exception as e:
            pass
            
    def handle_udev_event(self, action, device):
        """
        Handle a udev event
        """
        if action == 'add':
            if device.device_node is not None: 
                self.gui.show_notification("New USB device detected - Open file browser to explore it", action="skill.file-browser.openvoiceos.home", noticetype="transient", style="info")
            
        elif action == 'remove':
            if device.device_node is not None:
                self.gui.show_notification("A USB device was removed", noticetype="transient", style="info")

    @intent_file_handler("open.file.browser.intent")
    def show_home(self, message):
        """
        Show the file browser home page
        """
        self.gui.show_page("Browser.qml", override_idle=120)

    def handle_file(self, message):
        """ 
        Handle a file from the file browser Video / Audio
        """
        fileUrl = message.data.get("fileURL", "")
        # Determine if file is audio or video
        fileExtension = fileUrl.split(".")[-1]
        if fileExtension in self.audioExtensions:            
            media = {
                "match_confidence": 100,
                "media_type": MediaType.AUDIO,
                "length": 0,
                "uri": fileUrl,
                "playback": PlaybackType.AUDIO,
                "image": self.skill_location_path + "/ui/images/generic-audio-bg.jpg",
                "bg_image": self.skill_location_path + "/ui/images/generic-audio-bg.jpg",
                "skill_icon": "",
                "title": fileUrl.split("/")[-1],
                "skill_id": "skill-file-browser.openvoiceos"
            }
            playlist = [media]
            disambiguation = [media]
            self.bus.emit(Message("ovos.common_play.play", {"media": media, "playlist": playlist, "disambiguation": disambiguation}))
            self.gui.release()
            
        if fileExtension in self.videoExtensions:
            media = {
                "match_confidence": 100,
                "media_type": MediaType.VIDEO,
                "length": 0,
                "uri": fileUrl,
                "playback": PlaybackType.VIDEO,
                "image": self.skill_location_path + "/ui/images/generic-audio-bg.jpg",
                "bg_image": self.skill_location_path + "/ui/images/generic-audio-bg.jpg",
                "skill_icon": "",
                "title": fileUrl.split("/")[-1],
                "skill_id": "skill-file-browser.openvoiceos"
            }
            playlist = [media]
            disambiguation = [media]
            self.bus.emit(Message("ovos.common_play.play", {"media": media, "playlist": playlist, "disambiguation": disambiguation}))
            self.gui.release()
    
    def handle_folder_playlist(self, message):
        """
        Handle a folder from the file browser as a playlist
        """
        folderUrl = message.data.get("path", "")
        # Get all files in the folder
        files = os.listdir(folderUrl)
        # Create a playlist
        playlist = []
        for file in files:
            fileUrl = "file://" + folderUrl + "/" + file
            fileExtension = fileUrl.split(".")[-1]
            if fileExtension in self.audioExtensions:
                media = {
                    "match_confidence": 100,
                    "media_type": MediaType.AUDIO,
                    "length": 0,
                    "uri": fileUrl,
                    "playback": PlaybackType.AUDIO,
                    "image": self.skill_location_path + "/ui/images/generic-audio-bg.jpg",
                    "bg_image": self.skill_location_path + "/ui/images/generic-audio-bg.jpg",
                    "skill_icon": "",
                    "title": fileUrl.split("/")[-1],
                    "skill_id": "skill-file-browser.openvoiceos"
                }
                playlist.append(media)
            if fileExtension in self.videoExtensions:
                media = {
                    "match_confidence": 100,
                    "media_type": MediaType.VIDEO,
                    "length": 0,
                    "uri": fileUrl,
                    "playback": PlaybackType.VIDEO,
                    "image": self.skill_location_path + "/ui/images/generic-audio-bg.jpg",
                    "bg_image": self.skill_location_path + "/ui/images/generic-audio-bg.jpg",
                    "skill_icon": "",
                    "title": fileUrl.split("/")[-1],
                    "skill_id": "skill-file-browser.openvoiceos"
                }
                playlist.append(media)

        if len(playlist) > 0:
            media = playlist[0]
            disambiguation = playlist
            self.bus.emit(Message("ovos.common_play.play", {"media": media, "playlist": playlist, "disambiguation": disambiguation}))
            self.gui.release()
            
    def share_to_device_kdeconnect(self, message):
        """
        Share a file to a device using KDE Connect
        """
        file_url = message.data.get("file", "")
        device_id = message.data.get("deviceID", "")
        subprocess.Popen(["kdeconnect-cli", "--share", file_url, "--device", device_id])
    
    def stop(self):
        """
        Mycroft Stop Function
        """
        if self.udev_thread is not None:
            self.udev_thread.stop()
            self.udev_thread.join()

def create_skill():
    """
    Mycroft Create Skill Function
    """
    return FileBrowserSkill()

