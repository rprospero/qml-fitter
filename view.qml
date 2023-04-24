import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import Tutorial

ApplicationWindow{
    id: window
    visible: true
    title: "Fitter"

    FileDialog {
        id: fileDialog
        onAccepted: model.loadFile(selectedFile)
    }

    menuBar: MenuBar {
        Menu {
            title: "&File"
            Action {
                text: "&Open data"
                shortcut: StandardKey.Open
                onTriggered: fileDialog.open()
            }
            Action {
                text: "&Quit"
                shortcut: StandardKey.Quit
                icon.name: "application-exit"
                onTriggered: window.close()
            }
        }
    }

    Model {
        id: model
        intercept: intercept.text
        slope: slope.text
        x_min: x_min.text
        x_max: x_max.text
        imageWidth: main.width
        imageHeight: main.height
        onModelChanged: {
            console.log("Updating")
            main.update()
        }
    }

    ColumnLayout {
        id: options
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom

        Text { text: "Intercept" }
        TextField { 
            id: intercept 
            validator: DoubleValidator {}
            text: "1"
        }
        Text { text: "Slope" }
        TextField { 
            id: slope 
            validator: DoubleValidator {}
            text: "1"
        }
    }

    LiveImage {
        id: main
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.left: options.right

        image: model.image
    }
}