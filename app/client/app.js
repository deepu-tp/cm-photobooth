change = function(e) {

    // $('#tts').change(function(){ // Comment the above line and uncomment this to make the below script run on input field blur All the brackets, 20 lines below
      $('body').css('background-image', 'url(/loading.gif)');

      var url = ('http://api.flickr.com/services/rest/?method=flickr.photos.search'
              + '&api_key=b706170f0271cb3cb4b58ad38fb5ad6f'
              + '&text=' + $(this).val() + '&in_gallery=true'
              + '&format=json&nojsoncallback=1&sort=interestingness-desc'
              + '&safe_search=1')
        HTTP.get(url, function(err, res){
          var data = res.data
          $("#noimage").show();
          if(data.photos.photo[0].id) {
            $("#noimage").hide();
          }

          var img_url = ('http://api.flickr.com/services/rest/'
                         + '?method=flickr.photos.getSizes'
                         + '&api_key=b706170f0271cb3cb4b58ad38fb5ad6f'
                         + '&photo_id=' + data.photos.photo[0].id
                         + '&format=json&nojsoncallback=1')
          HTTP.get(img_url,
            function(err, res){
              var image = res.data
              var img_url = image.sizes.size[image.sizes.size.length - 1].source
              Session.set('id', data.photos.photo[0].id)
              Meteor.call('get_image_url', img_url, data.photos.photo[0].id,
                function(err, res){
                  console.log(img_url)
                  $('body').css('background-image',
                    'url(' + res.url + ')');
                })


            })

        })

    }

Template.image.rendered = function(){

  if(!this._rendered){
    Session.set('uid', Random.hexString(7))
    var voice = document.getElementById('tts');
    voice.onchange = change
    voice.onwebkitspeechchange = change
    this._rendered = true
  }
}

Template.image.events({
  'click #take_background' : function(){
    Meteor.call('take_background', Session.get('uid'), function(err, data){
      console.log(arguments)
    })
  },

  'click #take_both' : function(){
    Meteor.call('take_both', Session.get('uid'), function(err, data){
      console.log(arguments)
    })
  },

  'click #bs' : function(){
    Meteor.call('bs', Session.get('id'), Session.get('uid'), function(err, data){
      $('body').css('background-image',
      'url(' + data.url + ')');
    })
  },

  'click #reset' : function(){
    Session.set('id', null)
    Session.set('uid', Random.hexString(7))
    $('body').css('background', 'none');
  },

  'submit' : function(e, ui){
    e.preventDefault()
  }

})
