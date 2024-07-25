import curses

def display_colors(stdscr):
    curses.start_color()
    curses.use_default_colors()
    
    # Define the basic colors and 256 colors
    for i in range(256):
        curses.init_pair(i, i, -1)
    
    stdscr.clear()
    
    # Print basic colors
    stdscr.addstr(0, 0, "Basic Colors:", curses.A_BOLD)
    for i in range(8):
        stdscr.addstr(i + 1, 0, f"Color {i}: ", curses.color_pair(i))
        stdscr.addstr(i + 1, 15, "Sample", curses.color_pair(i))
    
    # Print 256 colors
    stdscr.addstr(10, 0, "256 Colors:", curses.A_BOLD)
    for i in range(256):
        x = i % 16
        y = 10 + (i // 16)
        stdscr.addstr(y, x * 10, f"Color {i}", curses.color_pair(i))
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(display_colors)
