import QtQuick
import QtQuick.Controls
import Tutorial

ApplicationWindow{
    visible: true
    title: "Fitter"

    Model {
        id: model
        intercept: intercept.text
    }

    Rectangle {
        id: main
        anchors.fill: parent
        color: "green"

        TextField {
            id: intercept
        }

        Text {
            text: model.y_min + "," + model.y_max
            anchors.centerIn: main
        }
    }
}