'use strict';
/* Services */


angular.module('FindecoUserService', ['FindecoService'])
    .factory('FindecoUserService', function (FindecoService) {
        var localData = {};
        var localSetContent = function(data) {
            localData.content = data;
            if ( angular.equals(localData.content,{}) ) {
                localData.isLoggedIn = false;
            } else {
                localData.isLoggedIn = true;
            }
        };
        return {
            data: localData,
            setContent: localSetContent,
            initialize: function(){
                FindecoService.get({action: '.json_loadUserSettings'}, function (data) {
                    if ( data.errorResponse != undefined ) {
                        return;
                    }
                    localSetContent(data.loadUserSettingsResponse);
                });
            }
        };
    });