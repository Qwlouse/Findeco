
findecoApp.filter('timeFromNow', function() {
        return function(input) {
            // uses http://momentjs.com/
            return moment(input).fromNow();
        }
    });