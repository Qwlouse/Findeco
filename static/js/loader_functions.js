function load(){
    $(document).ajaxStart(function() {
        $('#loading').show();
    });
    $(document).ajaxStop(function() {
        $('#loading').hide();
    });

    var box1 = BoxRegister.newBox();
    box1.show('center');

    // $.get('/Findeco/tests.php?.json_loadText/topic.1/subtopic.1',function(json){
    var json = {"loadTextResponse":{"paragraphs":[{"wikiText":"= Subsubtopic 1 =\r\nBlablabla.\r\nBlablubblubb.","path":"topic.1\/subtopic.1\/subsubtopic.1","isFollowing":1,"authorGroup":["author1","author2"]},{"wikiText":"= Subsubtopic 2 =\r\nBlablabla.\r\nBlablubblubb.","path":"topic.1\/subtopic.1\/subsubtopic2.1","isFollowing":1,"authorGroup":["author1","author3"]}],"isFollowing":1}};
    var data = new ClassData();
    data.load(json);
    box1.printData(data);
    // },'json');

    var box2 = BoxRegister.newBox();
    box2.show('right');
    var box3 = BoxRegister.newBox();
    box3.show('left');
    var box4 = BoxRegister.newBox();
    box4.show('swap',box3);
    var box5 = BoxRegister.newBox();
    box5.show('swap',box3);
}

window.onhashchange = function() {
    Controller.loadLocation(document.location.hash);
};

