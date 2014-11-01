
Google Chrome debugging
-----------------------

When debugging Google Chrome, it comes handy to see where the object was 
allocated without any debugger breakpoints. So I wrote this tiny function.
```cpp
// src\third_party\WebKit\Source\core\frame\LocalDOMWindow.cpp
#include "base/logging.h" 

// snip...

void LocalDOMWindow::rawDump(Element* element)
{
    if (!element) {
        VLOG(1) << "rawDump: element you trying to dump seems to be dead.";
        return;
    }

    VLOG(1) << "*** rawDump: " << element->localName().string().ascii().data() 
            << " at " << std::hex << element 
            << " (refCount = " << element->refCount() << ") ***";
}

void LocalDOMWindow::rawLog(const String& comment)
{
    VLOG(1) << comment.ascii().data();
}
```

Another function, rawLog(), is an oversimplified replacement for console.log() 
as a console functions seem to not guarantee execution in expected time (bug?).

Don't forget headers:
```cpp
// src\third_party\WebKit\Source\core\frame\LocalDOMWindow.h
	void rawDump(Element*);
    void rawLog(const String& comment);
```

And update IDL file:
```cpp
// src\third_party\WebKit\Source\core\frame\Window.idl
    void rawDump(Element element);
	void rawLog(DOMString comment);
```

Type in console rawDump(document.body) or any other element, and see log:
```
[78281:1291:1101/192857:VERBOSE1:LocalDOMWindow.cpp(1318)] *** rawDump: div at 0x4300d248 (refCount = 9) ***
[78281:1291:1101/192919:VERBOSE1:LocalDOMWindow.cpp(1318)] *** rawDump: a at 0x43054480 (refCount = 9) ***
[78281:1291:1101/192940:VERBOSE1:LocalDOMWindow.cpp(1314)] rawDump: element you trying to dump seems to be dead.
[78281:1291:1101/193003:VERBOSE1:LocalDOMWindow.cpp(1314)] rawDump: element you trying to dump seems to be dead.
[78281:1291:1101/193008:VERBOSE1:LocalDOMWindow.cpp(1318)] *** rawDump: body at 0x4300c000 (refCount = 3) ***
```