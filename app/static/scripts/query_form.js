// Wrap your code in this to make sure document loads BEFORE script.
$( document ).ready(function(){

  $("#query-form").submit(function(event){

    // Can't let it send normally
    event.preventDefault();


    //clear out result
    var resDiv = $("#query-response");
    resDiv.empty();

    var keyword1 = $("#keyword1").val()
      , keyword2 = $("#keyword2").val();

    // make phrases
    keyword1.replace(' ', '_');
    keyword2.replace(' ', '_');

    // stem
    keyword1 = stemmer(keyword1);
    keyword2 = stemmer(keyword2);

    var email = $('#email').val();

    var cloudSize = 10000;

    var numTopics = $('#num_topics').val();

    var formData = {
      'keywords': keyword1 + "," + keyword2,
      'cloud_size': cloudSize,
      'num_topics': numTopics,
    };

    if(email){
      formData['email'] = email;
    }

    console.log(formData);

    $.ajax({
      type:'POST',
      url:'/api/query',
      data: formData,
      dataType: 'json', // return type
      encode: true
    }).done(function(data){
      if(data.query_id){
        $("<div class='col-md-2 text-success text-right'>Query ID:</div>").appendTo(resDiv);
        var msg = $("<div class=col-md-10></div>");
        msg.append(data.query_id);
        msg.appendTo(resDiv);
      } else {
        $("<div class='col-md-2 text-danger text-right'>Error:</div>").appendTo(resDiv);
        $("<div class=col-md-10>Somethings Gone Wrong.</div>").appendTo(resDiv);
      }

      console.log(data);
    })
  });

});
