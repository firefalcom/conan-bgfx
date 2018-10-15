#include <bgfx/bgfx.h>

#ifdef LINUX
#include <X11/Xlib.h>
#endif

int main() {

#ifdef LINUX
    XInitThreads();
    return 0; // Init crashes in headless mode on Linux.
#endif

    if (!bgfx::init()) {
        // Since we don't have any platform data (window handle, etc) for it took into,
        // BGFX correctly fails to initialize. But we linked and ran, so test successful!
        // 		fprintf(stderr, "Unable to initialize graphics system (this is normal).\n");
        return 0;
    }

    bgfx::reset(640, 480, BGFX_RESET_VSYNC);
    bgfx::shutdown();

    return 0;
}
