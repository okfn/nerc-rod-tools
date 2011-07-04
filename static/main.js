jQuery(function ($) {
  $('.detail')
    .before('<p><a href="#" class="detail-toggle">Show details &raquo;</a></p>')
    .hide();
  
  $('.detail-toggle').toggle(function () {
    $(this).html("&laquo; Hide details")
           .parent().next().show();
  },
  function () {
     $(this).html("Show details &raquo;")
             .parent().next().hide();
  });
  
});