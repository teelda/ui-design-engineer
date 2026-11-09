# Surface-specific evidence

Choose the actual surface. Do not substitute a responsive browser preview for a native-device test.

| Surface | Exercise when available | Evidence limit |
|---|---|---|
| Web application | Browser navigation, keyboard, viewport/reflow, refresh, URL state, network/API errors, permissions, session expiry and multi-tab behavior. | A screenshot or source file cannot prove deployed behavior. |
| Native mobile | Device or simulator navigation/back, touch, safe areas, system keyboard, orientation, interruptions, notifications, poor connection, background/return and platform accessibility controls. | A web emulator does not prove native behavior; record OS/device/version. |
| Desktop application | Window resize, menus, keyboard shortcuts, file/open/save, drag/drop, offline state, notifications, multiple windows and OS permission prompts. | Source inspection does not prove packaging or OS integration. |

When only screenshots or source are available, assess visible/source-supported risks and list the interactions needing device testing. Apply current platform guidance only for the platform actually used; do not claim platform or accessibility certification from this checklist.
