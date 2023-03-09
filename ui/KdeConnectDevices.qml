// SPDX-FileCopyrightText: 2021 Aditya Mehra <aix.m@outlook.com>
//
// SPDX-License-Identifier: Apache-2.0

import QtQuick 2.15
import QtQuick.Layouts 1.15
import Qt.labs.folderlistmodel 2.15
import QtQuick.Controls 2.15 as Controls
import Mycroft 1.0 as Mycroft
import org.kde.kirigami 2.19 as Kirigami
import OVOSPlugin 1.0 as OVOSPlugin
import org.kde.kdeconnect 1.0 as KDEConnect
import Qt5Compat.GraphicalEffects

Rectangle {
    id: rootKdeConnectDeviceSelector
    color: Kirigami.Theme.backgroundColor
    property bool opened: false
    visible: opened ? 1 : 0
    enabled: opened ? 1 : 0
    width: parent.width * 0.8
    height: parent.height * 0.8
    radius: 6
    z: 200
    layer.enabled: true
    layer.effect: DropShadow {
        horizontalOffset: 0
        verticalOffset: 0
        radius: 10
        color: "black"
        samples: 16
    }

    function open() {
        opened = true
        imageViewer.close()
    }

    function close() {
        opened = false
    }

    KDEConnect.DevicesModel {
        id: devicesModel
    }

    Item {
        id: topDeviceModelArea
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: Mycroft.Units.gridUnit * 3

        Kirigami.Heading {
            text: qsTr("Select Device")
            color: Kirigami.Theme.textColor
            width: parent.width
            height: parent.height
            anchors.left: parent.left
            anchors.leftMargin: Mycroft.Units.gridUnit / 2
            anchors.verticalCenter: parent.verticalCenter
        }

        Kirigami.Separator {
            anchors.bottom: parent.bottom
            width: parent.width
            height: 1
            color: Kirigami.Theme.textColor
        }
    }

    ListView {
        anchors.top: topDeviceModelArea.bottom
        anchors.margins: Mycroft.Units.gridUnit / 2
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: bottomDeviceModelArea.top
        model: devicesModel
        
        delegate: Controls.Button {
            width: parent.width
            height: Mycroft.Units.gridUnit * 4
            text: name

            onClicked: {
                Mycroft.SoundEffects.playClickedSound(Qt.resolvedUrl("sounds/clicked.wav"))
                browserView.shareFile(deviceId)
                rootKdeConnectDeviceSelector.close()
            }
        }
    }

    Item {
        id: bottomDeviceModelArea
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: Mycroft.Units.gridUnit * 4

        Controls.Button {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.margins: Mycroft.Units.gridUnit / 2
            text: qsTr("Cancel")

            onClicked: {
                Mycroft.SoundEffects.playClickedSound(Qt.resolvedUrl("sounds/clicked.wav"))
                rootKdeConnectDeviceSelector.close()
            }
        }
    }
}
