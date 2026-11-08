#define UNICODE
#define _UNICODE
#include <windows.h>

#define ID_CLOSE 1001
#define ID_APP_ICON 1

static HFONT heading_font;
static HFONT body_font;
static HFONT small_font;
static HBRUSH background;
static HICON app_icon;

static void text(HDC dc, const wchar_t *value, RECT bounds, HFONT font, COLORREF color, UINT flags) {
    HGDIOBJ old_font = SelectObject(dc, font);
    SetBkMode(dc, TRANSPARENT);
    SetTextColor(dc, color);
    DrawTextW(dc, value, -1, &bounds, flags | DT_RTLREADING | DT_RIGHT | DT_NOPREFIX);
    SelectObject(dc, old_font);
}

static LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
    case WM_CREATE: {
        heading_font = CreateFontW(-25, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE, DEFAULT_CHARSET,
            OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY, DEFAULT_PITCH, L"Segoe UI");
        body_font = CreateFontW(-17, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, DEFAULT_CHARSET,
            OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY, DEFAULT_PITCH, L"Segoe UI");
        small_font = CreateFontW(-15, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, DEFAULT_CHARSET,
            OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY, DEFAULT_PITCH, L"Segoe UI");
        HWND button = CreateWindowW(L"BUTTON", L"بستن", WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_PUSHBUTTON,
            40, 302, 110, 36, window, (HMENU)(INT_PTR)ID_CLOSE,
            ((LPCREATESTRUCTW)lparam)->hInstance, NULL);
        SendMessageW(button, WM_SETFONT, (WPARAM)body_font, TRUE);
        return 0;
    }
    case WM_PAINT: {
        PAINTSTRUCT paint;
        HDC dc = BeginPaint(window, &paint);
        RECT client;
        GetClientRect(window, &client);
        FillRect(dc, &client, background);
        if (app_icon) DrawIconEx(dc, 40, 38, app_icon, 64, 64, 0, NULL, DI_NORMAL);
        text(dc, L"پوستهٔ بازسازی‌شده", (RECT){125, 37, 576, 78}, heading_font, RGB(242, 246, 255), DT_SINGLELINE | DT_VCENTER);
        text(dc, L"Nexida Loader  |  نسخهٔ اصلی: 1.2.9124", (RECT){125, 80, 576, 112}, small_font, RGB(153, 172, 200), DT_SINGLELINE | DT_VCENTER);
        text(dc, L"منطق برنامهٔ اصلی هنوز بازیابی نشده است.", (RECT){40, 145, 576, 179}, body_font, RGB(255, 209, 131), DT_SINGLELINE | DT_VCENTER);
        text(dc, L"این نسخه فقط با منابع بازیابی‌شده ساخته شده و عملکرد اصلی برنامه را ندارد.",
            (RECT){40, 190, 576, 245}, body_font, RGB(214, 225, 240), DT_WORDBREAK);
        text(dc, L"برای بازسازی عملکرد، اطلاعات بیشتری از برنامه لازم است.",
            (RECT){40, 255, 576, 284}, small_font, RGB(153, 172, 200), DT_SINGLELINE | DT_VCENTER);
        EndPaint(window, &paint);
        return 0;
    }
    case WM_COMMAND:
        if (LOWORD(wparam) == ID_CLOSE) { DestroyWindow(window); return 0; }
        break;
    case WM_DESTROY:
        if (heading_font) DeleteObject(heading_font);
        if (body_font) DeleteObject(body_font);
        if (small_font) DeleteObject(small_font);
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(window, message, wparam, lparam);
}

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE previous, PWSTR command_line, int show_command) {
    (void)previous; (void)command_line;
    background = CreateSolidBrush(RGB(16, 24, 38));
    if (!background) return 1;
    app_icon = (HICON)LoadImageW(instance, MAKEINTRESOURCEW(ID_APP_ICON), IMAGE_ICON, 64, 64, LR_DEFAULTCOLOR);
    WNDCLASSW wc = {0};
    wc.lpfnWndProc = window_proc;
    wc.hInstance = instance;
    wc.hCursor = LoadCursorW(NULL, IDC_ARROW);
    wc.hIcon = app_icon;
    wc.hbrBackground = background;
    wc.lpszClassName = L"NexidaRecoveryShell";
    if (!RegisterClassW(&wc)) { DeleteObject(background); return 1; }
    RECT rect = {0, 0, 616, 368};
    DWORD style = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX;
    AdjustWindowRect(&rect, style, FALSE);
    HWND window = CreateWindowW(wc.lpszClassName, L"Nexida - پوستهٔ بازسازی‌شده", style,
        CW_USEDEFAULT, CW_USEDEFAULT, rect.right - rect.left, rect.bottom - rect.top,
        NULL, NULL, instance, NULL);
    if (!window) { if (app_icon) DestroyIcon(app_icon); DeleteObject(background); return 1; }
    ShowWindow(window, show_command);
    UpdateWindow(window);
    MSG message;
    int result;
    while ((result = GetMessageW(&message, NULL, 0, 0)) > 0) {
        if (!IsDialogMessageW(window, &message)) {
            TranslateMessage(&message);
            DispatchMessageW(&message);
        }
    }
    if (app_icon) DestroyIcon(app_icon);
    DeleteObject(background);
    return result == -1 ? 1 : (int)message.wParam;
}
