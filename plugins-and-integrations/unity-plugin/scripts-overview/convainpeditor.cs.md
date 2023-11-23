---
description: ConvaiNPC Custom Editor Documentation
---

# ConvaiNPEditor.cs

#### Introduction

The `ConvaiNPC` Custom Editor within the Unity Editor environment is designed to manage and maintain states of Convai scripts, ensuring a smooth and error-free workflow, especially when changes are made to game components.

***

#### 1. Requirements

Before diving into the functionalities, ensure that you're working within the Unity Editor environment as the script specifically targets editor functionalities.

***

#### 2. Properties & Fields

**ConvaiNPCEditor**

* `_convaiNPC`: Reference to the `ConvaiNPC` component on which this custom editor operates.

**StateSaver**

* `RootDirectory`: Root directory path where the saved states of Convai scripts are stored.

***

#### 3. Methods & Utilities

**ConvaiNPCEditor**

* `OnEnable()`: Initializes the `_convaiNPC` reference.
* `OnInspectorGUI()`: Overridden inspector GUI to provide an "Apply changes" button, which, when clicked, confirms the user's decision and applies the changes.
* `ApplyChanges()`: Applies component changes based on the user's selection in the inspector.
* `ApplyComponent<T>()`: Applies or removes a specified component based on conditions. This function also handles saving or restoring component states.

**StateSaver**

* `SaveScriptState()`: Saves the state of all Convai scripts in the active scene.

**SaveSceneHook**

* `SceneSaved()`: Hooks into the Unity's `sceneSaved` event and invokes `SaveScriptState()`.

**EditorExtensions**

Utility extension methods to streamline the saving and restoring processes.

* `SaveStateToFile<T>()`: Saves the state of a specific component to a file.
* `RestoreStateFromFile<T>()`: Restores the state of a specific component from a file.
* `AddComponentSafe<T>()`: Safely adds a component to a GameObject.
* `GetSavePath()`: Generates the save path for a given script's state.

***

#### 4. Usage Guidelines

1. **Adding Components & Saving State**:
   * Once the `ConvaiNPC` component is attached to a GameObject, you'll see the customized inspector.
   * Adjust the settings and components as needed.
   * Click the "Apply changes" button to apply your modifications. The system will confirm your actions before proceeding.
   * The `SaveScriptState` utility will automatically save the state of all Convai scripts when the scene is saved.
2. **Restoring Component States**:
   * If a component was removed and needs to be added again, upon re-adding, the system will attempt to restore its state from the saved data.

***

#### 5. Troubleshooting

**Error when adding component**: If you receive an error when trying to add a component via the editor, ensure that there are no conflicts with other scripts or missing references.

**State restoration fails**: If the state restoration process fails for a component, check the saved file's integrity and the `RootDirectory` path.

> **Note**: Always ensure to have backups before making major changes or applying bulk operations.

\
