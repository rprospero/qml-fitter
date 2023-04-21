import QtQuick
import QtQuick.Controls

ApplicationWindow{
    visible: true
    title: "Fitter"
    Rectangle {
        id: main
        anchors.fill: parent
        color: "green"

        Text {
            text: "Hello World"
            anchors.centerIn: main
        }
    }
}