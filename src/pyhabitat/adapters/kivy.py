import os
import logging

logger = logging.getLogger(__name__)

def is_kivy_available() -> bool:
    """Check if the Kivy framework is installed and importable."""
    try:
        import kivy  # noqa: F401
        return True
    except Exception:
        return False

def is_android_kivy() -> bool:
    """Check if running natively inside an Android Kivy application."""
    # Fast path: check python-for-android environment indicators
    if any(k in os.environ for k in ("ANDROID_ARGUMENT", "ANDROID_ENTRYPOINT")):
        return True

    # Kivy platform path
    try:
        from kivy.utils import platform
        return platform == "android"
    except Exception:
        return False

def is_android_kivy_activity_active() -> bool:
    """Check if the Android PythonActivity context is initialized and active."""
    if not is_android_kivy():
        return False

    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        return getattr(PythonActivity, "mActivity", None) is not None
    except Exception as e:
        logger.debug("Failed to verify Android PythonActivity lifecycle: %s", e)
        return False

def launch_browser_in_kivy():
    if is_javascript_on_android_with_kivy():
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")
            Uri = autoclass("android.net.Uri")

            activity = PythonActivity.mActivity
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            activity.startActivity(intent)
            return True
        except Exception as e:
            logger.exception("Android JNI intent execution failed: %s", e)
            return False
