function TextCtrl($scope, $http) {

    $http.get('texts/kanon_izr.pt', {
        transformResponse: function (data) {
            // parsing PT into Javascript object.
            return _.map(data.split('\n\n'), function (rungStr) {
                var rungObj = {};
                _.forEach(rungStr.split('\n'), function (line) {
                    if (!line) {
                        return;
                    }
                    var match = line.match(/^([a-z]+) (.*)$/); // line format
                    if (!match) {
                        console.error("line does not match: ", line);
                        return;
                    }
                    var list = rungObj[match[1]] || [];
                    list.push(match[2]);
                    rungObj[match[1]] = list;
                });
                return rungObj;
            });
        }
    }).success(function (data) {
        console.log('success', data);
        $scope.rungs = data;
    });

    $scope.langs = ['pl', 'cu', 'el'];

    $scope.title = "text text";
}