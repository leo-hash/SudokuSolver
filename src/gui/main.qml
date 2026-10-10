import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


ApplicationWindow {
     id: window
    property var frontend: sudokuFrontend

    visible: true
    width: 600
    height: 700

    // variables to store selected field
    property int selectedRow: -1
    property int selectedColumn: -1



    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20

        GridLayout {

            rows: 9
            columns: 9

            rowSpacing: 0
            columnSpacing: 0

            Repeater {
                model: 81

                Rectangle {
                    // indexing variables for the grid
                    required property int index

                    property int row: Math.floor(index / 9)
                    property int column: index % 9

                    property int cellValue: window.frontend.getValue(row, column)
                    property bool invalidInput: false
                    property bool fixed:
                        window.frontend.isFixed(row, column)

                    id: cell
                    Layout.preferredWidth: 50
                    Layout.preferredHeight: 50

                    Timer {
                        id: invalidInputTimer
                        // 1.5 seconds
                        interval: 1500
                        repeat: false

                        onTriggered: cell.invalidInput = false
                    }

                    Connections {
                        target: window.frontend

                        function onCellChanged(changedRow, changedColumn, value) {
                            if (changedRow === row && changedColumn === column) {
                                cellValue = value
                            }
                        }

                        function onInvalidNumberInput(changedRow, changedColumn, err_message) {
                            if (changedRow === row && changedColumn === column) {
                                cell.invalidInput = true
                                // reset timer
                                invalidInputTimer.stop()
                                invalidInputTimer.start()
                            }
                        }
                    }

                    color: {
                        if (fixed) {
                            return "#eeeeee"
                        }

                        if (invalidInput){
                            return "#FFB3B3"
                        }

                        if (row === selectedRow &&
                            column === selectedColumn) {
                            return "#cce5ff"
                        }

                        return "white"
                    }

                    border.color: "black"
                    border.width: 1

                    Text {
                        anchors.centerIn: parent
                        text: cellValue === 0 ? "" : cellValue
                        font.pixelSize: 24
                        color: fixed ? "#222222" : "#3366cc"
                    }

                    MouseArea {
                        anchors.fill: parent
                        enabled: !fixed

                        onClicked: {
                            selectedRow = row
                            selectedColumn = column
                        }
                    }

                    // thick vertical lines
                    Rectangle {
                        visible: column === 2 || column === 5
                        width: 3
                        height: parent.height
                        color: "black"
                        anchors.right: parent.right
                        z: 2
                    }

                    // thick horizontal lines
                    Rectangle {
                        visible: row === 2 || row === 5
                        width: parent.width
                        height: 3
                        color: "black"
                        anchors.bottom: parent.bottom
                        z: 2
                    }

                }
            }
        }


        RowLayout {
            spacing: 5

            Repeater {
                model: 9

                Button {
                    // index for repeater
                    required property int index

                    text: index + 1

                    Layout.preferredWidth: 45
                    Layout.preferredHeight: 45

                    enabled: selectedRow >= 0 &&
                        selectedColumn >= 0 &&
                        window.frontend.getValue(selectedRow, selectedColumn) === 0

                    onClicked: {
                        if (selectedRow >= 0 &&
                            selectedColumn >= 0) {
                            var success = window.frontend.setValue(selectedRow, selectedColumn, index + 1)

                            if (success === false){
                                console.log("window.frontend.setValue failed")
                            }
                        }
                    }
                }
            }

            Button {
                text: "⌫"

                Layout.preferredWidth: 45
                Layout.preferredHeight: 45

                enabled: selectedRow >= 0 &&
                    selectedColumn >= 0 &&
                    window.frontend.getValue(selectedRow, selectedColumn) !== 0

                onClicked: {
                    if (selectedRow >= 0 &&
                        selectedColumn >= 0) {
                        window.frontend.setValue(selectedRow, selectedColumn, 0)
                    }
                }
            }
        }
    }
}