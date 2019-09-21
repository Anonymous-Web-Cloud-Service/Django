var BucketName = 'awc20190723';
var bucketRegion = 'ap-northeast-2';
var IdentityPoolId = 'ap-northeast-2:db593849-54e5-4054-934b-df7290753f21';

AWS.config.update({
  region: bucketRegion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId
  })
});

var s3 = new AWS.S3({
  apiVersion: '2006-03-01',
  params: {
    Bucket: BucketName
  }
});

function getHtml(template) {//javascript에서 바로 html을 출력할 수 있게 해주는 코드
      return template.join('\n');
}

function createBoard(boardName){//게시판 이름만 입력하면 생성됨
  boardName = boardName.trim();
  if (!boardName) {
    return alert('Album names must contain at least one non-space character.');
  }
  if (boardName.indexOf('/') !== -1) {
    return alert('Album names cannot contain slashes.');
  }
  var boardKey = encodeURIComponent(boardName) + '/';
  s3.headObject({
    Key: boardKey
  }, function (err, data) {
    if (!err) {
      return alert('Board already exists.');
    }
    if (err.code !== 'NotFound') {
      return alert('There was an error creating your Board: ' + err.message);
    }
    s3.putObject({
      Key: boardKey
    }, function (err, data) {
      if (err) {
        return alert('There was an error creating your Board: ' + err.message);
      }
      alert('Successfully created Board.');
      viewBorad(boardName);
    });
  });
}

function listBoard(){
  s3.listObjects({Delimiter: '/'}, function(err, data) {
    if (err) {
      return alert('There was an error listing your albums: ' + err.message);
    } else {
      var boards = data.CommonPrefixes.map(function(commonPrefix) {
        var prefix = commonPrefix.Prefix;
        var boardName = decodeURIComponent(prefix.replace('/', ''));
        return getHtml([
          '<li>',
            '<span onclick="deleteBoard(\'' + boardName + '\')">X</span>',
            '<span onclick="viewBoard(\'' + boardName + '\')">',
              boardName,
            '</span>',
          '</li>'
        ]);
      });
      var message = boards.length ? //길이가 0이면 : 뒤에 문장 실행
        getHtml([
          '<p>Click on an album name to view it.</p>',
          '<p>Click on the X to delete the album.</p>'
        ]) :
        getHtml([
         '<button onclick="createBoard(prompt(\'Enter Board Name:\'))">',
        'Create New Board',
        '</button>'
        ])
        ;
      var htmlTemplate = [
        '<h2>boards</h2>',
        message,
        '<ul>',
          getHtml(boards),
        '</ul>'
      ]
      document.getElementById('app').innerHTML = getHtml(htmlTemplate);
    }
  });
}

function viewBoard(boardName){
var boardKey = encodeURIComponent(boardName) + '//';
  s3.listObjects({
    Prefix: boardKey
  }, function (err, data) {
    if (err) {
      return alert('There was an error viewing your board: ' + err.message);
    }
    // 'this' references the AWS.Response instance that represents the response
    var href = this.request.httpRequest.endpoint.href;
    var bucketUrl = href + BucketName + '/';
    console.log('게시판', data.Contents);
    var files = data.Contents.map(function (file) {
      var fileKey = file.Key;
      var fileUrl = bucketUrl + encodeURIComponent(fileKey);
      return getHtml([

        '<div>',
        '<span>',
        '<a href =', fileUrl, '>',
        'test',
        '</a>',
        '<button onclick = "deleteObject(\'' + boardName + "','" + fileKey + '\')">',
        'delete',
        '</button>',
        '</span>',
        '<span>',
        fileKey.replace(boardKey, ''),
        '</span>',
        '</span>',
        '</div>',
      ]);
    });
    var message = files.length ?
        '<p>Click on the X to delete the photo</p>' :
        '<p>You do not have any file in this board. Please add File.</p>';
    var htmlTemplate = [
      '<h2>',
      'Album: ' + boardName,
      '</h2>',
      message,
      '<div>',
      getHtml(files),
      '</div>',
      '<input id="fileUpload" type="file">',
      '<button id="addFile" onclick="uploadObject(\'' + boardName + '\' )">',
      'Upload File',
      '</button>',
      '<button onclick="listBoard()">',
      'Back To Boards',
      '</button>',
    ]
    document.getElementById('app').innerHTML = getHtml(htmlTemplate);
  });
}

function uploadObject(boardName){

    var files = document.getElementById('fileUpload').files;
      if (!files.length) {//파일 갯수가 0이면 밑에 알람 발생
        return alert('Please choose a file to upload first.');
      }
      var file = files[0];
      var fileName = file.name;
      var boardKey = encodeURIComponent(boardName) + '//';

      var fileKey = boardKey + fileName;
      s3.putObject({
        Key: fileKey,
        Body: file,
        ACL: 'public-read',
        Metadata : {'file_name' : fileName}
      }, function (err, data) {
        if (err) {
          console.log(err)
          return alert('There was an error uploading your file: ' +  err.message);
        }
        alert('Successfully uploaded file.');
        viewBoard(boardName);
      });
}

function viewObject(){

}

function downloadObject(url){
  document.location.href = String(url);
}

function listObject(){

}


function searchBorad(){

}

function searchObject(){

}

function deleteObject(boardName, fileKey) {
  s3.deleteObject({
    Key: fileKey
  }, function (err, data) {
    if (err) {
      return alert('There was an error deleting your photo: ' + err.message);
    }
    alert('Successfully deleted file.');
    viewBoard(boardName);
  });
}

function deleteAlbum(albumName) {
  var albumKey = encodeURIComponent(albumName) + '/';
  s3.listObjects({
    Prefix: albumKey
  }, function (err, data) {
    if (err) {
      return alert('There was an error deleting your album: ', err.message);
    }
    var objects = data.Contents.map(function (object) {
      return {
        Key: object.Key
      };
    });
    s3.deleteObjects({
      Delete: {
        Objects: objects,
        Quiet: true
      }
    }, function (err, data) {
      if (err) {
        return alert('There was an error deleting your album: ', err.message);
      }
      alert('Successfully deleted album.');
      listAlbums();
    });
  });
}

function deleteBoard(boardName) {
  var boardKey = encodeURIComponent(boardName) + '/';
  s3.listObjects({
    Prefix: boardKey
  }, function (err, data) {
    if (err) {
      return alert('There was an error deleting your board: ' +  err.message);
    }
    var objects = data.Contents.map(function (object) {
      return {
        Key: object.Key
      };
    });
    s3.deleteObjects({
      Delete: {
        Objects: objects,
        Quiet: true
      }
    }, function (err, data) {
      if (err) {
        return alert('There was an error deleting your album: ' + err.message);
      }
      alert('Successfully deleted board.');
      listAlbums();
    });
  });
}