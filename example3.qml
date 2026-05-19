// Copyright (C) 2024 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

// NOTE: This is a demonstration application developed for showcasing Qt's capabilities.
// For official reference code and documentation, please visit the Qt documentation portal
// at https://doc.qt.

/*
 * Main QML file
 *
 * Entry point of the QML application. Defines the primary structure,
 * initializes window related properties, and loads the main views and
 * components. The same QML works on both native and web targets and
 * automatically initializes the needed facilities for input and rendering.
 */

// QtQuick is the standard library of QML types and functionality. It includes
// visual types, interactive types, animations, models and views, particle
// effects and shader effects.
import QtQuick
// Directories need to be imported before the contained components can be used.
// Components that are in the same directory can be used directly.
import "home"
import "media"
import "my-car"
import "settings"
import "widgets"

Item {
    // Ids can be used to refer to this component and access its properties
    id: mainWindow

    readonly property real px: Math.min(width, height) / 540
    // Dynamic data that controls how widgets are shown. The affected widgets
    // are reactively updated when these values are modified.
    property bool showWidgets: true
    property bool showSettings: false
    property int toolbarIndex: 0

    anchors.fill: parent

    /*
    ------------------------------------------------------
    ------------------------------------------------------
    ------------------------------------------------------


    CROSS-PLATFORM CAPABILITIES

    - This file serves as the unified entry point for your application,
        enabling deployment across different devices and operating systems.

    - By keeping all core logic and UI definitions in one place, you can
        achieve consistent user experiences on car dashboards, mobile phones,
        or other form factors with minimal adjustments.


    ------------------------------------------------------
    ------------------------------------------------------
    ------------------------------------------------------
    */

    // These components are defined in the root so they can be used
    // in this component and all child components.
    DData {
        id: dData
    }

    DemoAnimation {
        id: demoAnimation
    }

    DStyle {
        id: dStyle
    }

    Media {
        id: media
    }

    /*
    ------------------------------------------------------
    ------------------------------------------------------
    ------------------------------------------------------


    PERFORMANCE AND MEMORY OPTIMIZATION

    How to see this in action:
    1. Navigate between the different views of the application
    2. See how performance intensive views don’t affect the overall performance of the application.
    This is especially important when running on low performance hardware.


    - Demonstrates how lazy initialization and memory-efficient layouts improve performance in the car configurator.
    - Best practices include:
        - Using Loader for deferred initialization of less frequently accessed components.
        - Employing static positioning over dynamic anchors in non-dynamic layouts.
        - Reducing redundant bindings for performance-critical paths.
        - If performance-critical components (e.g., CarModel) become
            too large, loaders or lightweight object hierarchies can be used to reduce
            memory consumption.


    ------------------------------------------------------
    ------------------------------------------------------
    ------------------------------------------------------
    */

    Item {
        id: mainViewContainer

        // Anchors can be used to robustly position widgets.
        anchors.left: parent.left
        anchors.right: widgetsView.left
        anchors.top: parent.top
        anchors.bottom: mainToolbar.top

        HomeView {
            // The `show` property is reactively updated when the toolbarIndex
            // changes and the correct view gets shown.
            show: mainWindow.toolbarIndex == 0
        }

        MediaView {
            show: mainWindow.toolbarIndex == 1
        }

        MyCarView {
            show: mainWindow.toolbarIndex == 2
        }
    }

    AssistantPopup {
        id: assistantPopup

        width: mainToolbar.width
        height: 120 * px
    }

    MainToolbar {
        id: mainToolbar

        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: widgetsView.left
        // MainToolbar utilizes signals, and they can be listened to with a
        // property `on<SignalName>`. Signals can be used to flexibly
        // communicate between components.
        onAssistantButtonClicked: assistantPopup.show()
    }

    WidgetsView {
        id: widgetsView

        anchors.right: parent.right
        show: showWidgets
    }

    SettingsView {
        id: settingsView

        anchors.left: parent.left
        show: showSettings
    }

    
}
