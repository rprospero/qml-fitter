import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Tutorial

ApplicationWindow{
    visible: true
    title: "Fitter"

    Model {
        id: model
        intercept: intercept.text
        slope: slope.text
        x_min: x_min.text
        x_max: x_max.text
    }

    ColumnLayout {
        id: options
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom

        Text { text: "Intercept" }
        TextField { id: intercept }
        Text { text: "Slope" }
        TextField { id: slope }

        Text { text: "x_min" }
        TextField { id: x_min }
        Text { text: "x_max" }
        TextField { id: x_max }
    }

    Image {
        id: main
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.left: options.right

        source: model.image
    }
}