// -*- coding: utf-8 -*-
// This file is part of Invenio.
// Copyright (C) 2013 CERN.
//
// Invenio is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License as
// published by the Free Software Foundation; either version 2 of the
// License, or (at your option) any later version.
//
// Invenio is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Invenio; if not, write to the Free Software Foundation, Inc.,
// 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}

$(document).ready(function(){

    var url_base = "/admin/holdingpen";
    var url_restart_record = url_base + "/restart_record";
    var url_restart_record_prev = url_base + "/restart_record_prev";
    var url_continue = url_base + "/continue_record";

    function bootstrap_alert(message) {
        $('#alert_placeholder').html('<div class="alert"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>');
    }

    $('#restart_button').on('click', function() {
        bwo_id = $(this).attr('name');
        console.log(bwo_id);
        jQuery.ajax({
            url: url_restart_record + "?bwobject_id=" + bwo_id,
            success: function(json){
                bootstrap_alert('Object restarted');
            }
        });
    });

    $('#restart_button_prev').on('click', function() {
        bwo_id = $(this).attr('name');
        console.log(bwo_id);
        jQuery.ajax({
            url: url_restart_record_prev + "?bwobject_id=" + bwo_id,
            success: function(json){
                bootstrap_alert('Object restarted from previous task');        
            }
        });
    });

    $('#continue_button').on('click', function() {
        bwo_id = $(this).attr('name');
        console.log(bwo_id);
        jQuery.ajax({
            url: url_continue + "?bwobject_id=" + bwo_id,
            success: function(json){
                bootstrap_alert('Object continued from next task');        
            }
        });
    });

    window.setTimeout(function() {
        $("#alert_placeholder").fadeTo(500, 0).slideUp(500, function(){
        });
    }, 2000);

    if ( window.addEventListener ) {
        $("div.btn-group[name='data_version']").bind('click', function(event){
            version = event.target.name;
        });
    }

    bwoid = getURLParameter('bwobject_id');

});
