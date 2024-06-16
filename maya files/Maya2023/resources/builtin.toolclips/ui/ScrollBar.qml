import QtQuick 2.0
import com.autodesk.toolclips.qml 1.0

/** \file ScrollBar.qml

Adds a scroll bar to the right or bottom of flickable element. 

Properties
----------

* **flickable**: <br/>The flickable to which the scrollbar is attached to, must be set.

* **vertical**: <br/>True for vertical scroll bar, false for horizontal

* **hide_at_rest**: <br/>True if the scroll bar should hide when not scrolling.

* **scroll_bar_width**: <br/>Thickness of the scrollbar, in pixels.

*/


Item {
    id: scrollbar;
    width: (handleSize + 2);
    visible: (flickable.visibleArea.heightRatio < 1.0);
    anchors {
        top: flickable.top;
        right: flickable.right;
        bottom: flickable.bottom;
        margins: 1;
    }

    property Flickable flickable : null;
    property int       handleSize: 20;

   Binding {
        target: handle;
        property: "y";
        value: (flickable.contentY * clicker.drag.maximumY / (flickable.contentHeight - flickable.height));
        when: (!clicker.drag.active);
    }
    Binding {
        target: flickable;
        property: "contentY";
        value: (handle.y * (flickable.contentHeight - flickable.height) / clicker.drag.maximumY);
        when: (clicker.drag.active || clicker.pressed);
    }
    Rectangle {
        id: backScrollbar;
        radius: 2;
        antialiasing: true;
        color: Qt.rgba(55/255, 55/255, 55/255, 1.0);
        anchors { fill: parent; }

        MouseArea {
            anchors.fill: parent;
            onClicked: { }
        }
    }
    MouseArea {
        id: btnUp;
        height: width;
        anchors {
            top: parent.top;
            left: parent.left;
            right: parent.right;
        }
        onClicked: {
			flickable.contentY = Math.max (flickable.contentY - (flickable.height / 4), 0);
		}

        Text {
            text: "V";
            color: "#A4A4A4";
            rotation: -180;
            anchors.centerIn: parent;
        }
    }
    MouseArea {
        id: btnDown;
        height: width;
        anchors {
            left: parent.left;
            right: parent.right;
            bottom: parent.bottom;
        }
        onClicked: {
			flickable.contentY = Math.min (flickable.contentY + (flickable.height / 4), flickable.contentHeight - flickable.height);
		}

        Text {
            text: "V";
            color: "#A4A4A4";
            anchors.centerIn: parent;
        }
    }
    Item {
        id: groove;
        clip: true;
        anchors {
            fill: parent;
            topMargin: (1 + btnUp.height );
            leftMargin: 0;
            rightMargin: 0;
            bottomMargin: (1 + btnDown.height );
        }

        MouseArea {
            id: clicker;
            drag {
                target: handle;
                minimumY: 0;
                maximumY: (groove.height - handle.height);
                axis: Drag.YAxis;
            }
            anchors { fill: parent; }
            onClicked: { flickable.contentY = (mouse.y / groove.height * (flickable.contentHeight - flickable.height)); }
        }
        Item {
            id: handle;
            height: Math.max (20, (flickable.visibleArea.heightRatio * groove.height));
            anchors {
                left: parent.left;
                right: parent.right;
            }

            Rectangle {
                id: backHandle;
                color: "#5D5D5D";
                opacity: 1.0;
                anchors { fill: parent; }
				radius: 8

                Behavior on opacity { NumberAnimation { duration: 150; } }
            }
        }
    }
}
