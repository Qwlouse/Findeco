/****************************************************************************************
 * Copyright (c) 2014 Klaus Greff, Maik Nauheim, Johannes Merkert                       *
 *                                                                                      *
 * This file is part of Findeco.                                                        *
 *                                                                                      *
 * Findeco is free software; you can redistribute it and/or modify it under             *
 * the terms of the GNU General Public License as published by the Free Software        *
 * Foundation; either version 3 of the License, or (at your option) any later           *
 * version.                                                                             *
 *                                                                                      *
 * Findeco is distributed in the hope that it will be useful, but WITHOUT ANY           *
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A      *
 * PARTICULAR PURPOSE. See the GNU General Public License for more details.             *
 *                                                                                      *
 * You should have received a copy of the GNU General Public License along with         *
 * Findeco. If not, see <http://www.gnu.org/licenses/>.                                 *
 ****************************************************************************************/
/****************************************************************************************
 * This Source Code Form is subject to the terms of the Mozilla Public                  *
 * License, v. 2.0. If a copy of the MPL was not distributed with this                  *
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.                             *
 ****************************************************************************************/

describe('FindecoUserService', function() {
    var userService, httpBackend, rootScope;
    var userInfo = {
        displayName: 'hugo',
        description: 'beschreibung'
    };

    var adminInfo = {
        displayName: 'admin',
        description: 'darfalles'
    };

    var userSettings = {
        rsskey: 'abcdefg',
        email: 'hugo@abc.de',
        followees: [{displayName: 'ben'}],
        wantsMailNotification:true
    };

    var loadUserSettingsResponse = {
        loadUserSettingsResponse: {
            userInfo: userInfo,
            userSettings: userSettings
        }
    };

    beforeEach(function (){
        angular.mock.module('FindecoUserService');
        angular.mock.inject(function($httpBackend, $rootScope, User) {
            userService = User;
            httpBackend = $httpBackend;
            rootScope = $rootScope;
        });
        spyOn(rootScope, '$broadcast');
    });

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });


    ///////////////// Initialization ///////////////////////////////////////////
    describe('Initialization', function() {
        it('should call loadSettings', function () {
            httpBackend.expectGET('/.json_loadUserSettings/').respond(406, '');
            httpBackend.flush();
        });
    });

    describe('FindecoUserService', function () {
        beforeEach(function (){
            httpBackend.expectGET('/.json_loadUserSettings/').respond(406, '');
            httpBackend.flush();
        });

        var loginResponse = {
            loginResponse: {
                userInfo: userInfo,
                userSettings: userSettings
            }
        };
        var adminLoginResponse = {
            loginResponse: {
                userInfo: adminInfo,
                userSettings: userSettings
            }
        };
        var loadAdminSettingsResponse = {
            loadUserSettingsResponse: {
            userInfo: adminInfo,
            userSettings: userSettings
        }
    };

        var logoutResponse = {logoutResponse: {}};
        var accountRegistrationResponse = {accountRegistrationResponse: {}};
        var accountActivationResponse = {accountActivationResponse: {}};
        var accountResetConfirmationResponse = {accountResetConfirmationResponse: {}};
        var emailChangeConfirmationResponse = {emailChangeConfirmationResponse: {}};
        var recoverByMailResponse = {accountResetRequestByMailResponse: {}};
        var recoverByUsernameResponse = {accountResetRequestByNameResponse: {}};
        var markUserResponse = {
            markUserResponse: {
                followees: [{'displayName': 'albert'}, {'displayName': 'ben'}]
            }
        };
        var deleteUserResponse = {deleteUserResponse: {}};
        var changePasswordResponse = {changePasswordResponse: {}};
        var storeSettingsResponse = {storeSettingsResponse: {}};

        //////////////// Login ////////////////////////////////////////////////////
        describe('login function', function() {
            it('should set the userInfo details after successful login', function () {
                httpBackend.expectPOST('/.json_login/').respond(loginResponse);
                //make the call.
                userService.login('hugo', '1234');
                httpBackend.flush();

                expect(userService.isLoggedIn).toBe(true);
                expect(userService.isAdmin).toBe(false);
                expect(userService.displayName).toBe(userInfo.displayName);
                expect(userService.description).toBe(userInfo.description);
                expect(userService.rsskey).toBe(userSettings.rsskey);
                expect(userService.email).toBe(userSettings.email);
                expect(userService.followees).toEqual(userSettings.followees);
                expect(userService.wantsMailNotification).toBe(userSettings.wantsMailNotification);
            });

            it('should set the userInfo details after successful admin login', function () {
                httpBackend.expectPOST('/.json_login/').respond(adminLoginResponse);
                //make the call.
                userService.login('admin', '1234');
                httpBackend.flush();

                expect(userService.isLoggedIn).toBe(true);
                expect(userService.isAdmin).toBe(true);
                expect(userService.displayName).toBe(adminInfo.displayName);
                expect(userService.description).toBe(adminInfo.description);
            });
        });

        ///////////////// Logout ///////////////////////////////////////////////////
        describe('logout function', function() {
            it('should remove the user details after successful logout', function () {
                httpBackend.whenGET('/.json_logout/').respond(logoutResponse);
                userService.logout();
                httpBackend.flush();
                expect(userService.isLoggedIn).toBe(false);
                expect(userService.displayName).toBe('');
                expect(userService.description).toBe('');
                expect(userService.rsskey).toBe('');
                expect(userService.email).toBe('');
                expect(userService.followees).toEqual([]);
            });
        });

        ///////////////// Registration /////////////////////////////////////////////
        describe('Registration', function() {
            describe('register function', function() {
                it('should call the .json_accountRegistration api function', function() {
                    httpBackend.expectPOST('/.json_accountRegistration/', {
                            displayName: 'albert',
                            password: '4321',
                            emailAddress: 'alb@rt.de'})
                        .respond(accountRegistrationResponse);
                    //make the call.
                    userService.register('albert', '4321', 'alb@rt.de');
                    httpBackend.flush();
                });
            });

            describe('activate function', function() {
                it('should call the .json_accountActivation api function', function() {
                    httpBackend.expectPOST('/.json_accountActivation/', {
                                activationKey: 'ABCDEFG01234567890'})
                        .respond(accountActivationResponse);

                    userService.activate('ABCDEFG01234567890');
                    httpBackend.flush();
                });
            });
        });

        ///////////////// Confirm Email Change /////////////////////////////////////

        describe('confirmEmail function', function() {
            it('should call the .json_emailChangeConfirmation api function', function() {
                httpBackend.expectPOST('/.json_emailChangeConfirmation/', {
                            activationKey: 'ABCDEFG01234567890'})
                    .respond(emailChangeConfirmationResponse);

                userService.confirmEmail('ABCDEFG01234567890');
                httpBackend.flush();
            });
        });

        ///////////////// Recovery /////////////////////////////////////////////////
        describe('Recovery', function() {
            describe('recoverByMail function', function() {
                it('should call the .json_accountResetRequestByMail api function', function() {
                    httpBackend.expectPOST('/.json_accountResetRequestByMail/', {
                                emailAddress: 'alb@rt.de'})
                        .respond(recoverByMailResponse);

                    userService.recoverByMail('alb@rt.de');
                    httpBackend.flush();
                });
            });

            describe('recoverByUsername function', function() {
                it('should call the .json_accountResetRequestByName api function', function() {
                    httpBackend.expectPOST('/.json_accountResetRequestByName/', {
                                displayName: 'albert'})
                        .respond(recoverByUsernameResponse);

                    userService.recoverByUsername('albert');
                    httpBackend.flush();
                });
            });

            describe('confirm function', function() {
                it('should call the .json_accountResetConfirmation api function', function() {
                    httpBackend.expectPOST('/.json_accountResetConfirmation/', {
                                activationKey: 'ABCDEFG01234567890'})
                        .respond(accountResetConfirmationResponse);

                    userService.confirm('ABCDEFG01234567890');
                    httpBackend.flush();
                });
            });
        });

        describe('markUser function', function() {
            it('should call the .json_markUser api function with markType and displayName', function() {
                httpBackend.expectPOST('/.json_markUser/follow/albert', {})
                    .respond(markUserResponse);
                httpBackend.expectPOST('/.json_markUser/unfollow/ben', {})
                    .respond(markUserResponse);

                userService.markUser('follow', 'albert');
                userService.markUser('unfollow', 'ben');
                httpBackend.flush();
            });

            it('should update the userInfo with new followees', function() {
                httpBackend.expectPOST('/.json_markUser/follow/albert', {})
                    .respond(markUserResponse);
                userService.markUser('follow', 'albert');
                httpBackend.flush();

                expect(userService.followees).toEqual([
                    {
                        displayName: 'albert',
                        isFollowing: 2,
                        path: 'albert'
                    },
                    {
                        displayName: 'ben',
                        isFollowing: 2,
                        path: 'ben'
                    }])
            });

            it('should broadcast the UserMarked event', function() {
                httpBackend.expectPOST('/.json_markUser/follow/albert', {})
                    .respond(markUserResponse);
                userService.markUser('follow', 'albert');
                httpBackend.flush();
                expect(rootScope.$broadcast).toHaveBeenCalledWith('UserMarked');
            });
        });

        describe('loadSettings function', function() {
            it('should initialize with a .json_loadUserSettings call', function () {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(406, '');
                userService.loadSettings();
                httpBackend.flush();
            });

            it('should initialize user if loadUserSettings succeeds', function () {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                expect(userService.isLoggedIn).toBe(true);
                expect(userService.isAdmin).toBe(false);
                expect(userService.displayName).toBe(userInfo.displayName);
                expect(userService.description).toBe(userInfo.description);
                expect(userService.rsskey).toBe(userSettings.rsskey);
                expect(userService.email).toBe(userSettings.email);
                expect(userService.followees).toEqual([{
                    displayName: 'ben',
                    isFollowing:2,
                    path:'ben'
                }]);
                expect(userService.wantsMailNotification).toBe(userSettings.wantsMailNotification);
            });

            it('should initialize isAdmin if loadUserSettings for admin succeeds', function () {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadAdminSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                expect(userService.isLoggedIn).toBe(true);
                expect(userService.isAdmin).toBe(true);
                expect(userService.displayName).toBe(adminInfo.displayName);
                expect(userService.description).toBe(adminInfo.description);
            });

            it('should have empty user details if loadUserSettings does not succeed', function () {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(406, '');
                userService.loadSettings();
                httpBackend.flush();
                expect(userService.isLoggedIn).toBe(false);
                expect(userService.displayName).toBe('');
                expect(userService.description).toBe('');
                expect(userService.rsskey).toBe('');
                expect(userService.email).toBe('');
                expect(userService.followees).toEqual([]);
            });
        });

        describe('isChanged function', function() {
            it('should return false for not logged-in user', function() {
                expect(userService.hasUnsavedChanges()).toBeFalsy();
                userService.displayName = 'herbert';
                expect(userService.hasUnsavedChanges()).toBeFalsy();
            });

            it('should return false for logged-in but unchanged user', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                expect(userService.hasUnsavedChanges()).toBeFalsy();
            });

            it('should return false for just logged-in user', function() {
                httpBackend.expectPOST('/.json_login/').respond(loginResponse);
                userService.login('hugo', '1234');
                httpBackend.flush();
                expect(userService.hasUnsavedChanges()).toBeFalsy();
            });

            it('should return true for logged-in user with changed name', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.displayName = 'changedName';
                expect(userService.hasUnsavedChanges()).toBeTruthy();
            });

            it('should return true for logged-in user with changed description', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.description = 'changedDescription';
                expect(userService.hasUnsavedChanges()).toBeTruthy();
            });

            it('should return true for logged-in user with changed email', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.email = 'changedEMail';
                expect(userService.hasUnsavedChanges()).toBeTruthy();
            });

            it('should return true for logged-in user with changed wantsMailNotification', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.wantsMailNotification = false;
                expect(userService.hasUnsavedChanges()).toBeTruthy();
            });
        });

        describe('resetChanges function', function() {
            it('should undo changes to displayName', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.displayName = 'changedName';
                userService.resetChanges();
                expect(userService.displayName).toBe('hugo');
            });

            it('should undo changes to description', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.description = 'changedDescription';
                userService.resetChanges();
                expect(userService.description).toBe('beschreibung');
            });

            it('should undo changes to email', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.email = 'changedEmail';
                userService.resetChanges();
                expect(userService.email).toBe('hugo@abc.de');
            });

            it('should undo changes to wantsMailNotification', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.wantsMailNotification = false;
                userService.resetChanges();
                expect(userService.wantsMailNotification).toBeTruthy();
            });

        });

        describe('deleteAccount function', function() {
            it('should call the .json_deleteUser api function', function() {
                httpBackend.expectPOST('/.json_deleteUser/')
                    .respond(deleteUserResponse);
                userService.deleteAccount();
                httpBackend.flush();
            });
        });

        describe('changePassword function', function() {
            it('should call the .json_changePassword api function', function() {
                httpBackend.expectPOST('/.json_changePassword/', {
                    password: 'newPassword'
                }).respond(changePasswordResponse);
                userService.changePassword('newPassword');
                httpBackend.flush();
            });
        });

        describe('isFollowing function', function() {
            it('should return true if name is in followees list', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                expect(userService.isFollowing('ben')).toBeTruthy();
            });

            it('should return false if name is not in followees list', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                expect(userService.isFollowing('paul')).toBeFalsy();
            });
        });

        describe('storeSettings function', function() {
            it('should call the .json_storeSettings api function', function() {
                httpBackend.expectPOST('/.json_storeSettings/')
                    .respond(storeSettingsResponse);
                userService.storeSettings();
                httpBackend.flush();
            });

            it('should POST the current settings', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.displayName = 'mightyHugo';
                httpBackend.expectPOST('/.json_storeSettings/', {
                    displayName: 'mightyHugo',
                    description: 'beschreibung',
                    email: 'hugo@abc.de',
                    wantsMailNotification: true})
                    .respond(storeSettingsResponse);
                userService.storeSettings();
                httpBackend.flush();
            });

            it('on success there should be no changes', function() {
                httpBackend.expectGET('/.json_loadUserSettings/').respond(loadUserSettingsResponse);
                userService.loadSettings();
                httpBackend.flush();
                userService.displayName = 'Simon';
                expect(userService.hasUnsavedChanges()).toBeTruthy();
                httpBackend.expectPOST('/.json_storeSettings/')
                    .respond(storeSettingsResponse);
                userService.storeSettings();
                httpBackend.flush();
                expect(userService.hasUnsavedChanges()).toBeFalsy();
            });


        });



    });
});
