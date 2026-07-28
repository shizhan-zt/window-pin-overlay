import ctypes,ctypes.wintypes
u=ctypes.windll.user32;k=ctypes.windll.kernel32;g=ctypes.windll.gdi32;dwm=ctypes.windll.dwmapi
u.SetWindowPos.argtypes=[ctypes.wintypes.HWND,ctypes.wintypes.HWND,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_uint]
u.GetForegroundWindow.restype=ctypes.wintypes.HWND;u.GetDesktopWindow.restype=ctypes.wintypes.HWND
u.CreateWindowExW.restype=ctypes.wintypes.HWND;u.DefWindowProcW.restype=ctypes.c_ssize_t
u.LoadCursorW.restype=ctypes.c_void_p;g.GetStockObject.restype=ctypes.c_void_p;k.GetModuleHandleW.restype=ctypes.c_void_p
u.SetProcessDpiAwarenessContext.argtypes=[ctypes.c_void_p];u.SetProcessDpiAwarenessContext.restype=ctypes.wintypes.BOOL
try:u.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
except:pass
u.CreateWindowExW.argtypes=[ctypes.wintypes.DWORD,ctypes.wintypes.LPCWSTR,ctypes.wintypes.LPCWSTR,ctypes.wintypes.DWORD,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.wintypes.HWND,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
u.SetTimer.argtypes=[ctypes.wintypes.HWND,ctypes.c_size_t,ctypes.c_uint,ctypes.c_void_p];u.SetTimer.restype=ctypes.c_size_t
u.ShowWindow.argtypes=[ctypes.wintypes.HWND,ctypes.c_int];u.DestroyWindow.argtypes=[ctypes.wintypes.HWND]
u.IsWindow.argtypes=[ctypes.wintypes.HWND];u.IsWindowVisible.argtypes=[ctypes.wintypes.HWND]
u.GetClassNameW.argtypes=[ctypes.wintypes.HWND,ctypes.wintypes.LPWSTR,ctypes.c_int]
u.GetWindowRect.argtypes=[ctypes.wintypes.HWND,ctypes.POINTER(ctypes.wintypes.RECT)]
u.GetDpiForWindow.argtypes=[ctypes.wintypes.HWND];u.GetSystemMetricsForDpi.argtypes=[ctypes.c_int,ctypes.c_uint];u.GetSystemMetricsForDpi.restype=ctypes.c_int;u.InvalidateRect.argtypes=[ctypes.wintypes.HWND,ctypes.c_void_p,ctypes.wintypes.BOOL]
u.MonitorFromWindow.argtypes=[ctypes.wintypes.HWND,ctypes.wintypes.DWORD];u.MonitorFromWindow.restype=ctypes.c_void_p
u.DefWindowProcW.argtypes=[ctypes.wintypes.HWND,ctypes.c_uint,ctypes.wintypes.WPARAM,ctypes.wintypes.LPARAM]
k.CreateMutexW.argtypes=[ctypes.c_void_p,ctypes.wintypes.BOOL,ctypes.wintypes.LPCWSTR];k.CreateMutexW.restype=ctypes.wintypes.HANDLE
k.CloseHandle.argtypes=[ctypes.wintypes.HANDLE]
dwm.DwmGetWindowAttribute.restype=ctypes.c_long
dwm.DwmGetWindowAttribute.argtypes=[ctypes.wintypes.HWND,ctypes.c_uint,ctypes.c_void_p,ctypes.c_uint]
HT=ctypes.wintypes.HWND(-1);HN=ctypes.wintypes.HWND(-2);TOP=ctypes.wintypes.HWND(0);F=1|2|0x10
SZ=24;POLL=8;WM_T=0x0113;TID=1;EXISTS=183;MUTEX='Local\\DingziPluginOverlay'
NS=1;NM=2;NZ=4;NA=0x10;SHOW=0x40;NOACT=0x08000000

class MONITORINFO(ctypes.Structure):
 _fields_=[('cbSize',ctypes.wintypes.DWORD),('rcMonitor',ctypes.wintypes.RECT),('rcWork',ctypes.wintypes.RECT),('dwFlags',ctypes.wintypes.DWORD)]
u.GetMonitorInfoW.argtypes=[ctypes.c_void_p,ctypes.POINTER(MONITORINFO)]

def st(h,o):
 if not h or not u.IsWindow(h):return 0
 return u.SetWindowPos(h,HT if o else HN,0,0,0,0,F)
def fg():return u.GetForegroundWindow()
def vl(h):return bool(u.IsWindow(h))
def vs(h):return bool(u.IsWindowVisible(h))
def wn(h):
 b=ctypes.create_unicode_buffer(32);u.GetClassNameW(h,b,32)
 return b.value
def rc(h):
 r=ctypes.wintypes.RECT();u.GetWindowRect(h,ctypes.byref(r))
 return r.left,r.top,r.right,r.bottom
def fr(h):
 r=ctypes.wintypes.RECT()
 try:
  if dwm.DwmGetWindowAttribute(h,9,ctypes.byref(r),ctypes.sizeof(r))==0 and r.right>r.left:return r.left,r.top,r.right,r.bottom
 except:pass
 return rc(h)
def mt(h):
 m=u.MonitorFromWindow(h,2);i=MONITORINFO();i.cbSize=ctypes.sizeof(i)
 if m and u.GetMonitorInfoW(m,ctypes.byref(i)):return i.rcMonitor.top
 return rc(h)[1]
def dp(h):
 try:return u.GetDpiForWindow(h)/96.0
 except:
  dc=u.GetDC(0);d=g.GetDeviceCaps(dc,88);u.ReleaseDC(0,dc);return d/96.0
def sz(h):return max(18,round(SZ*dp(h)))
def mp(h):
 r=ctypes.wintypes.RECT()
 o=rc(h);w=fr(h)
 z=sz(h)
 try:
  if dwm.DwmGetWindowAttribute(h,5,ctypes.byref(r),ctypes.sizeof(r))==0 and r.right>r.left:
   if 0<=r.left<r.right<=o[2]-o[0] and 0<=r.top<r.bottom<=o[3]-o[1]:
    return o[0]+r.left-z-int(6*dp(h)),max(mt(h),o[1]+r.top+max(0,(r.bottom-r.top-z)//2))
 except:pass
 d=int(96*dp(h))
 try:bw=u.GetSystemMetricsForDpi(30,d);bh=u.GetSystemMetricsForDpi(31,d)
 except:bw=int(30*dp(h));bh=int(23*dp(h))
 return w[2]-3*bw-z-int(6*dp(h)),max(mt(h),w[1]+max(0,(bh-z)//2))
def shell_popup():
 for c in ('NotifyIconOverflowWindow','TopLevelWindowForOverflowXamlIsland'):
  h=u.FindWindowW(c,None)
  if h and vs(h):return 1
 return 0

WCP=ctypes.WINFUNCTYPE(ctypes.c_ssize_t,ctypes.wintypes.HWND,ctypes.c_uint,ctypes.wintypes.WPARAM,ctypes.wintypes.LPARAM)

class WNDCLASSEXW(ctypes.Structure):
 _fields_=[('cbSize',ctypes.c_uint),('style',ctypes.c_uint),('lpfnWndProc',WCP),('cbClsExtra',ctypes.c_int),('cbWndExtra',ctypes.c_int),('hInstance',ctypes.c_void_p),('hIcon',ctypes.c_void_p),('hCursor',ctypes.c_void_p),('hbrBackground',ctypes.c_void_p),('lpszMenuName',ctypes.wintypes.LPCWSTR),('lpszClassName',ctypes.wintypes.LPCWSTR),('hIconSm',ctypes.c_void_p)]

class PAINTSTRUCT(ctypes.Structure):
 _fields_=[('hdc',ctypes.c_void_p),('fErase',ctypes.wintypes.BOOL),('rcPaint',ctypes.wintypes.RECT),('fRestore',ctypes.wintypes.BOOL),('fIncUpdate',ctypes.wintypes.BOOL),('rgbReserved',ctypes.c_byte*32)]

u.RegisterClassExW.argtypes=[ctypes.POINTER(WNDCLASSEXW)];u.RegisterClassExW.restype=ctypes.c_ushort
u.BeginPaint.argtypes=[ctypes.wintypes.HWND,ctypes.POINTER(PAINTSTRUCT)];u.BeginPaint.restype=ctypes.c_void_p
u.EndPaint.argtypes=[ctypes.wintypes.HWND,ctypes.POINTER(PAINTSTRUCT)]
u.CreatePopupMenu.restype=ctypes.c_void_p;u.AppendMenuW.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_size_t,ctypes.wintypes.LPCWSTR]
u.TrackPopupMenu.argtypes=[ctypes.c_void_p,ctypes.c_uint,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.wintypes.HWND,ctypes.c_void_p];u.TrackPopupMenu.restype=ctypes.c_uint
u.DestroyMenu.argtypes=[ctypes.c_void_p];u.GetCursorPos.argtypes=[ctypes.POINTER(ctypes.wintypes.POINT)]
u.MessageBoxW.argtypes=[ctypes.wintypes.HWND,ctypes.wintypes.LPCWSTR,ctypes.wintypes.LPCWSTR,ctypes.c_uint];u.MessageBoxW.restype=ctypes.c_int
u.FindWindowW.argtypes=[ctypes.wintypes.LPCWSTR,ctypes.wintypes.LPCWSTR];u.FindWindowW.restype=ctypes.wintypes.HWND
g.CreateSolidBrush.argtypes=[ctypes.wintypes.DWORD];g.CreateSolidBrush.restype=ctypes.c_void_p
g.SelectObject.argtypes=[ctypes.c_void_p,ctypes.c_void_p];g.SelectObject.restype=ctypes.c_void_p
g.Ellipse.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
g.Rectangle.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
g.CreatePen.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.wintypes.DWORD];g.CreatePen.restype=ctypes.c_void_p
g.MoveToEx.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_void_p];g.LineTo.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
g.DeleteObject.argtypes=[ctypes.c_void_p]
u.GetDC.argtypes=[ctypes.wintypes.HWND];u.GetDC.restype=ctypes.c_void_p
u.ReleaseDC.argtypes=[ctypes.wintypes.HWND,ctypes.c_void_p];g.GetDeviceCaps.argtypes=[ctypes.c_void_p,ctypes.c_int]

class Ov:
 def __init__(s):
   s.sv=0;s.pin=0;s.ov=0;s.my=[];s._lx=-9999;s._ly=-9999;s._cls=0;s.z=SZ
   inst=k.GetModuleHandleW(None);cn='DZP'+str(id(s))
   wc=WNDCLASSEXW()
   s._proc=WCP(s._wp)
   wc.cbSize=ctypes.sizeof(wc);wc.style=0;wc.lpfnWndProc=s._proc
   wc.hInstance=inst;wc.hCursor=u.LoadCursorW(0,32512)
   wc.hbrBackground=g.GetStockObject(5)
   wc.lpszClassName=cn
   u.RegisterClassExW(ctypes.byref(wc))
   s.ov=u.CreateWindowExW(0x80|NOACT,cn,'',0x80000000,-10000,-10000,SZ,SZ,0,0,inst,None)
   u.ShowWindow(s.ov,0)
   s.my=[s.ov]
   # Desktop class names to skip
   s._cls=['#32769','Progman','WorkerW','SysListView32','Shell_TrayWnd','NotifyIconOverflowWindow']

 def _hide(s):
  if s.ov and u.IsWindowVisible(s.ov):u.ShowWindow(s.ov,0)

 def _quit(s,h):
  if u.MessageBoxW(h,'确定退出钉子插件吗？','钉子插件',4|0x20)==6:
   if s.pin and s.sv and vl(s.sv):st(s.sv,0)
   u.PostQuitMessage(0)

 def _wp(s,h,m,w,l):
  if m==WM_T:
   n=fg()
   if shell_popup():
    s._hide()
    return 0
   if n in s.my:
    if not s.pin:s._hide()
    return 0
   # Skip desktop/taskbar windows
   if not n or wn(n)in s._cls:
    if not s.pin:s.sv=0;s._hide()
    return 0
   if s.pin and s.sv:
    if not vl(s.sv)or not vs(s.sv):
     s.pin=0;s.sv=0;u.ShowWindow(s.ov,0)
     return 0
    x,y=mp(s.sv);z=sz(s.sv)
    if x!=s._lx or y!=s._ly or z!=s.z:
     s._lx=x;s._ly=y;s.z=z
    u.SetWindowPos(s.ov,HT,s._lx,s._ly,s.z,s.z,NA|SHOW)
    if not u.IsWindowVisible(s.ov):u.ShowWindow(s.ov,8)
   else:
    if n and vl(n)and vs(n)and n!=u.GetDesktopWindow()and n not in s.my:
     x,y=mp(n);z=sz(n)
     if s.sv!=n or x!=s._lx or y!=s._ly or z!=s.z:
      s.sv=n;s.pin=0;s._lx=x;s._ly=y;s.z=z
      u.SetWindowPos(s.ov,HT,x,y,z,z,NA|SHOW)
      s._dr()
     elif not u.IsWindowVisible(s.ov):
      u.SetWindowPos(s.ov,HT,s._lx,s._ly,s.z,s.z,NA|SHOW)
   return 0
  if m==0x0021:return 3
  if m==0x0201:
   if s.pin:
    if s.sv and vl(s.sv):st(s.sv,0)
    u.SetWindowPos(s.ov,HT,s._lx,s._ly,s.z,s.z,NA|SHOW);s.pin=0;s._dr()
   else:
    h2=s.sv if(s.sv and vl(s.sv))else fg()
    if h2 and vl(h2)and vs(h2)and h2 not in s.my and h2!=u.GetDesktopWindow()and wn(h2)not in s._cls:
      if st(h2,1):s.sv=h2;s.pin=1;x,y=mp(h2);s._lx=x;s._ly=y;s.z=sz(h2);u.SetWindowPos(s.ov,HT,x,y,s.z,s.z,NA|SHOW);s._dr()
   return 0
  if m==0x0203:
   s._quit(h)
   return 0
  if m==0x0204:
   pm=u.CreatePopupMenu()
   u.AppendMenuW(pm,0,101,'退出钉子')
   pt=ctypes.wintypes.POINT();u.GetCursorPos(ctypes.byref(pt))
   cmd=u.TrackPopupMenu(pm,0x0100|0x0002,pt.x,pt.y,0,s.ov,None)
   u.DestroyMenu(pm)
   if cmd==101:
    s._quit(h)
   return 0
  if m==0x0111:
   if (w&0xFFFF)==101:
    s._quit(h)
   return 0
  if m==0x000F:
   ps=PAINTSTRUCT()
   if not u.BeginPaint(h,ctypes.byref(ps)):return 0
   hdc=ps.hdc
   cv=0xeb6325 if s.pin else 0xb8a394
   z=s.z;p=g.CreatePen(0,max(1,round(z/12)),cv);old=g.SelectObject(hdc,p)
   a=int(z*.30);b=int(z*.70);t=int(z*.22);m=int(z*.43);q=int(z*.61);c=z//2
   g.MoveToEx(hdc,a,t,None);g.LineTo(hdc,b,t);g.LineTo(hdc,int(z*.60),m);g.LineTo(hdc,int(z*.74),q);g.LineTo(hdc,int(z*.26),q);g.LineTo(hdc,int(z*.40),m);g.LineTo(hdc,a,t)
   g.MoveToEx(hdc,c,q,None);g.LineTo(hdc,c,int(z*.83))
   g.SelectObject(hdc,old);g.DeleteObject(p)
   u.EndPaint(h,ctypes.byref(ps))
   return 0
  return u.DefWindowProcW(h,m,w,l)

 def _dr(s):
  u.InvalidateRect(s.ov,None,0)

def main():
 mutex=k.CreateMutexW(None,0,MUTEX)
 if not mutex:return
 if k.GetLastError()==EXISTS:
  u.MessageBoxW(0,'钉子插件已在运行。','钉子插件',0x40)
  k.CloseHandle(mutex)
  return
 ch=k.GetConsoleWindow()
 if ch:u.ShowWindow(ch,0)
 ov=Ov()
 u.MessageBoxW(0,'钉子插件已启动。\n单击钉子切换置顶，右键可退出。','钉子插件',0x40)
 u.SetTimer(ov.ov,TID,POLL,None)
 h=fg()
 if h and vl(h)and vs(h)and h not in ov.my and h!=u.GetDesktopWindow()and wn(h)not in ov._cls:
  ov.sv=h;x,y=mp(h);ov._lx=x;ov._ly=y;ov.z=sz(h)
  u.SetWindowPos(ov.ov,HT,x,y,ov.z,ov.z,NA|SHOW)
 msg=ctypes.wintypes.MSG()
 while u.GetMessageW(ctypes.byref(msg),0,0,0)>0:
  u.TranslateMessage(ctypes.byref(msg));u.DispatchMessageW(ctypes.byref(msg))
 u.DestroyWindow(ov.ov)
 k.CloseHandle(mutex)

if __name__=='__main__':main()
