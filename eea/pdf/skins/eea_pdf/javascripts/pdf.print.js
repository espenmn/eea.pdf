/*
FIX for How do I avoid a page break immediately after a header
http://stackoverflow.com/questions/9238868/how-do-i-avoid-a-page-break-immediately-after-a-header
*/

jQuery(document).ready(function($){
    var $content_core = $('#content-core');
    $content_core.find('h2').each(function(i, e){
      if (!$(e).closest('.cover').length){
        $(e).nextUntil('h2').andSelf().wrapAll('<div class="nobreak">');
      }
    });
    $content_core.find('h3').each(function(i, e){
      if (!$(e).closest('.nobreak, .keyMessage').length){
        $(e).nextUntil('h3').andSelf().wrapAll('<div class="nobreak">');
      }
    });
    /* Fix #28298, empty div.pageBreak cause segmentation fault in wkhtmltopdf */
    $content_core.find('div.pageBreak').each(function(i, e){
      $(e).html("&nbsp;");
    });

    // within collection change h1 to h4 to increment one step
    var $folder_titles = $(".pdf-folder-title");
    $folder_titles.each(function(idx, el) {
       var $el = $(el);
       var $parent = $el.parent();
       var $h1 = $parent.find('h1:not(.pdf-folder-title)');
       var $h2 = $parent.find('h2');
       var $h3 = $parent.find('h3');
       var $h4 = $parent.find('h4');
       $($h1, $h2, $h3, $h4).each(function(idx, el) {
            var $el = $(el);
            var incremented_header = window.parseInt(el.tagName[1], 10);
            incremented_header += 1;
            var tagName = "<h" + incremented_header + " />";
            var $replacement = $(tagName, {"class": el.className,
                                            id: el.id,
                                            text: el.innerHTML});
            $el.replaceWith($replacement);
       });
    });
});
