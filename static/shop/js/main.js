$( function() {
   $( "#slider-range" ).slider({
     range: true,
     min: 0,
     max: 800,
     values: [ 100, 400 ],
     slide: function( event, ui ) {
       $( "#amount" ).val( ui.values[ 0 ] );
       $( "#amountRight" ).val( ui.values[ 1 ] );
     }
   });
   $( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ));
   $( "#amountRight" ).val( $( "#slider-range" ).slider( "values", 1 ));

 } );



 $(function() {
  $( "#button" ).click(function() {
    $( "#button" ).addClass( "onclic", 250, validate);
  });

  function validate() {
    setTimeout(function() {
      $( "#button" ).removeClass( "onclic" );
      $( "#button" ).addClass( "validate", 450, callback );
    }, 2250 );
  }
    function callback() {
      setTimeout(function() {
        $( "#button" ).removeClass( "validate" );
      }, 1250 );
    }
  });
