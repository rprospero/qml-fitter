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

        Text { text: "x_min" }
        TextField { 
            id: x_min
            validator: DoubleValidator {}
            text: "-5"
        }
        Text { text: "x_max" }
        TextField { 
            id: x_max
            validator: DoubleValidator {}
            text: "5"
        }
    }

    GraphImage {
        id: main
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.left: options.right

        model: model
    }
}