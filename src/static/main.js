/*
 * this file need the following js files:
 * jQuery-1.6.2.js    http://jquery.com/
 * base64.js    http://www.webtoolkit.info/djs/webtoolkit.base64.js
 * jquery.tmpl.min.js    http://jquery.com/
 *
*/

var myAjax = {
    preUrl: '/api/',
    setAuthorization: function(req){
        self = this ;
        var user =  $.cookie('userid');
        var pass= $.cookie('secretkey');
        var auth = "Basic " + Base64.encode(user + ':' + pass);  //Base64 is in base64.js
        req.setRequestHeader('Authorization', auth);
    },
    error: function(jqXHR, textStatus, errorThrown){
        alert(errorThrown);
    },
    getJSON: function(url,donefun){
        self = this ;
        $.ajax({
            url : self.preUrl + url,
            dataType : 'json',
            beforeSend : self.setAuthorization,
            error : self.error
        })
        .done(donefun);
    },
    post: function(url,data,donefun){
        self = this ;
        $.ajax({
            url : self.preUrl + url,
            type : 'POST',
            data : data,
            beforeSend : self.setAuthorization,
            error : self.error
        })
        .done(donefun);
    },
    put: function(url,data,donefun){
        self = this ;
        data.__method='PUT';
        $.ajax({
            url : self.preUrl + url,
            type : 'POST',
            data : data,
            beforeSend : self.setAuthorization,
            error : self.error
        })
        .done(donefun);
    },
    del: function(url,donefun){
        self = this ;
        data.__method = 'DELETE';
        $.ajax({
            url : self.preUrl + url,
            type : 'POST',
            beforeSend : self.setAuthorization,
            error : self.error
        })
        .done(donefun);
    },
    putBody: function(url,data,donefun){
        self = this ;
        $.ajax({
            url : self.preUrl + url,
            type : 'POST',
            data : data,
            beforeSend : self.setAuthorization,
            error : self.error
        })
        .done(donefun);
    }
};

var myUI = {
    init: function(){
        self = this;
        $('#btn_toggle').bind('click',self.toggle)

        $("#groups").delegate("li", "mouseover", function(){
                $(this).addClass('mover');
            });
        $("#groups").delegate("li", "mouseleave", function(){
                $(this).removeClass('mover');
            });

        $("#ulnotes").delegate("li", "mouseover", function(){
                $(this).addClass('mover');
            });
        $("#ulnotes").delegate("li", "mouseleave", function(){
                $(this).removeClass('mover');
            });
        $("#ulnotes").delegate("li", "click", function(){
                var href = $(this).children('a').attr('href');
                location.href = href;
            });

        $("#openednotes").delegate("li", "mouseover", function(){
               //$(this).addClass('mover');
            });
        $("#openednotes").delegate("li", "mouseleave", function(){
               // $(this).removeClass('mover');
            });

        $("#openednotes").delegate("span", "click", function(){
                var noteid = 1; //
                //$(this).parent().
                $(this).parent().remove();
                noteUI.saveopenedstatus(noteid);
            });
    },
    toggle:function(){
        $('#col1').toggle();
        $('#col2').toggle();
    },
    resizecloumn:function(){}
};

var groupUI = {
    init: function(){
        var self = this ;
        $.template("groups_Template", '<a href="#g=${id}">${name}</a> <span>${notescount}</span>');
        var strform ='<form id="group_form"><input name="groupid" type="hidden" value="${id}" /><input name="name" type="text" value="${name}" /><input name="notescount" type="hidden" value="${notescount}" /></form>';

        $.template("createform_Template",'<li>' + strform + '</li>');
        $.template("editform_Template",strform);

/*
        self.resize();
        $(window).resize(function(){
            self.resize();
        }); */



        $('#btn_newgroup').bind('click',self.create)
        $("#groups").delegate("input[type='text']", "change", self.save);
        $("#groups").delegate("input[type='text']", "blur", self.cancel);

        $("#groups").delegate("li", "click", function(event){
                if(event.target.nodeName=='LI') {
                    var href = $(this).children('a').attr('href');
                    if(typeof href !== "undefined"){
                        self.edit(this);
                    }
                }

            });
    },

    resize: function(){
        var h = $(window).height();
        h=500;
        $('#col1').css('height',h);
        $('#col2').css('height',h);
        $('#col3').css('height',h);
        $('#txtnote').css('height',h);
    },

    create: function(){
        myAjax.post('group/0',{name:'new group'} , function(groupid){
            $.tmpl("createform_Template", {id:groupid,name:'new group',notescount:'0'}).appendTo( "#groups" );
        });
    },

    cancel: function(self){
                var form = $(this).parent();
                var nvs = $(form).serializeArray();
                var groupid = nvs[0].value;
                var groupname = $.trim(nvs[1].value);  //var self = this ;var v = self._getformvalues(input);
                var count = nvs[2].value

                var strhtml = $.tmpl("groups_Template", {id:groupid,name:groupname,notescount:count})
                $(form).parent().html(strhtml);
    },

    save: function(){
        var form = $(this).parent();
        var nvs = $(form).serializeArray();
        var groupid = nvs[0].value;
        var groupname = $.trim(nvs[1].value);
        var count = nvs[2].value

        var url='group/' + groupid;
        myAjax.put(url,{'name':groupname},function(id){
            var strhtml = $.tmpl("groups_Template", {id:groupid,name:groupname,notescount:count})
            $(form).parent().html(strhtml);
        });
    },

    edit: function(element){
        var str= $(element).html();
        if(str.indexOf('<form')!= -1){
            return;
        }

        var value =  $(element).find("a").text();  //$(element).children().text();
        var href = $(element).find("a").attr('href');
        var gid = href.split('=')[1];
        var count= $(element).find("span").text();

        $(element).html($.tmpl("editform_Template", {id:gid,name:value,notescount:count}))
        $(element).contents().find("[type='text']").focus();
    },

    drop: function(){
        var noteid = $('#noteid').val();
        var url='/group/'+ noteid;
        myAjax.del(url,function(){
            alert('fail');
        });
    }
};

var noteUI ={
    openednotes:[],

    init: function(){
        var self = this ;
        $.template("notes_Template", '<li><a id="notesumary_${id}" href="#n=${id}">${summary.substr(0,15)}</a></li>');
        $.template("openednote_Template", '<li><a id="oo${id}" href="#n=${id}">${summary}</a> <span>X</span></li>');
        $('#btn_newnote').bind('click',self.create);
        $('#txtnote').bind('change',self.save);
        $('#btn_deletenote').bind('click',self.drop);
    },
    create:function(){
        var url='note/0';
        var groupid = $('#selectedgroupid').val();
        var strNote = 'New Note';

        myAjax.post(url, {'groupid':groupid,'notes':strNote},
                        function(noteid){
                            $('#noteid').val(noteid);
                            $('#note_groupid').val(groupid);
                            $('#txtnote').val('New Note');

                            var note = {id:noteid,summary:strNote.substr(0,15)};
                            $.tmpl("notes_Template", note).prependTo( "#ulnotes" );
                            $.tmpl( "openednote_Template", note).appendTo("#openednotes");
                        });
    },

    list: function(hash){ //noraml, deleted, opened?
        var gid = hash.split('=')[1];

        $('#selectedgroupid').val(gid);
        $('.select').removeClass('select');
        $('#g'+gid).addClass('select');

        var url = 'notes/' + gid;
        myAjax.getJSON(url,function(notes){
                    $( "#ulnotes" ).empty();
                    $.tmpl( "notes_Template", notes).appendTo("#ulnotes");
                });
    },
    open:  function(hash){
        var self = this;
        var noteid = hash.split('=')[1];

        var exist = false;
        var note = $.each(noteUI.openednotes, function() {
             if(this.id== noteid){
                 exist = true;
                 return this;
             }
        });

        var url = 'note/' + noteid;
        myAjax.getJSON(url,function(note){
                        if(!exist){
                            noteUI.openednotes.push(note); //
                            note.summary = note.summary.substr(0,15)
                            $.tmpl( "openednote_Template", note).appendTo("#openednotes");
                        }

                        $('#noteid').val(note.id);
                        $('#note_groupid').val(note.groupid);
                        $('#txtnote').val(note.notes);

                        noteUI.saveopenedstatus();
                    });

    },
    save: function(){
        //create new or update an exist note
        var noteid = $('#noteid').val();
        var url='note/'+ noteid;
        var strNote = $('#txtnote').val();

        myAjax.put(url, {'groupid':$('#note_groupid').val(),'notes':strNote},function(){
                    $('#notesumary_' + noteid).text(strNote.substr(0,15));
                    $('#oo' + noteid).text(strNote.substr(0,15));
                });
    },
    drop: function(){
        var noteid = $('#noteid').val();
        var url='note/'+ noteid;
        myAjax.del(url,function(){
            alert('delete');
        });
    },
    saveopenedstatus:function(id){
        //myAjax.putBody('notes/opened','',function(){});
    }

};

var hashChange = {
    hashs:[],
    init:function(){
        var self = this;
        if ("onhashchange" in window){
            window.onhashchange = function () {
                self.changed(window.location.hash);
            }
        }
        else {
            var storedHash = window.location.hash;
            window.setInterval(function () {
                if (window.location.hash != storedHash) {
                    storedHash = window.location.hash;
                    self.changed(storedHash);
                }
            }, 100);
        }
    },
    changed:function(hash){
        var self = this;
        var hashs = self.hashs;
        if ((hashs.length % 2) != 0) {
            throw "mappings length is " + hashs.length + '. the lenght must be odd.';
        }
        var pairs_count = hashs.length / 2;
        for (var i = 0; i <= pairs_count; i = i + 2) {
            var pattern = new RegExp('^'+ hashs[i]+'$', 'ig');
            if (pattern.test(hash)) {
                hashs[i + 1](hash.substr(1)); //run the match function
                break;
            }
        }
    }
};


hashChange.hashs = ['#g=\\d+',noteUI.list,
   '#n=\\d+',noteUI.open];

$(function(){
    hashChange.init();
    myUI.init();
    groupUI.init();
    noteUI.init();
});


