# Pagination

The footer of every DataTable: a `small` summary in `muted-foreground` on the left ("Showing 26–50 of 1,204"), a rows-per-page select, and on the right previous/next ghost buttons (28px) with the current page as a `secondary` chip. For large sets the system prefers cursor paging (previous/next only) over numbered pages; numbered pages appear only when the total is known and under 50 pages. Keyboard: the buttons are real buttons; disabled at the ends. The consumer provides range, total, page size options and handlers.
