import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts
import Tutorial

ApplicationWindow{
    id: window
    visible: true
    title: "Fitter"
    width: 640
    height: 480

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
        onImageChanged: {
            main.update()
        }
    }

    GridLayout {
        id: options
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        columns: 2

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
        Text { text: "Chi Squared" }
        Text { text: model.chiSquared }
        Button { 
            width: parent.width
            text: "Fit"
            onClicked: {
                model.fitData()
                intercept.text = model.intercept
                slope.text = model.slope
            }
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