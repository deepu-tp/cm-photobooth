Meteor.startup(function () {
  // code to run on server at startup
});



Meteor.methods({
  'get_image_url' : function(url, id){
    var result = HTTP.post('http://localhost:5000/get_image_url', {
      'params' : {
        'url' : url,
        'id' : id
      }
    })
    console.log(result)
    return {url : 'http://localhost:5000/' + result.data.url}
  },

  'take_background' : function(id){
    var result = HTTP.post('http://localhost:5000/take_background', {
      'params' : {
        'uid' : id
      }
    })
    return {url : 'http://localhost:5000/' + result.data.url}
  },


  'take_both' : function(id){
    var result = HTTP.post('http://localhost:5000/take_both', {
      'params' : {
        'uid' : id
      }
    })
    return {url : 'http://localhost:5000/' + result.data.url}
  },


  'bs' : function(id, uid){
    console.log(id, uid)
    var result = HTTP.post('http://localhost:5000/bs', {
      'params' : {
        'id' : id,
        'uid' : uid
      }
    })
    console.log(result)
    return {url : 'http://localhost:5000/' + result.data.url}

  }
})
