class CacheClient{
    constructor(url,$http){
        self.url=url;
        self.$http=$http;
    }
    
    getBanks(successCallback,errorCallback){
        self.$http({
            method: 'GET',
            url: self.url+'/banks'
            }).then(function _successCallback(response) {
                console.log(response);
                successCallback(response.data.data);
            }, function _errorCallback(response) {
                console.log("Error",response);
                if (errorCallback!==undefined)
                    errorCallback(response);
            });
    }
    
    getElements(bank,successCallback,errorCallback){
        self.$http({
            method: 'GET',
            url: self.url+'/bank/'+bank+'/entries'
            }).then(function _successCallback(response) {
                console.log(response);
                successCallback(response.data.data);
            }, function _errorCallback(response) {
                console.log("Error",response);
                if (errorCallback!==undefined)
                    errorCallback(response);
            });
    }
    
    getValue(bank,entry,successCallback,errorCallback){
        self.$http({
            method: 'GET',
            url: self.url+'/bank/'+bank+'/entry/'+entry
            }).then(function _successCallback(response) {
                console.log(response);
                successCallback(response.data.data);
            }, function _errorCallback(response) {
                console.log("Error",response);
                if (errorCallback!==undefined)
                    errorCallback(response);
            });
    }
    
    setValue(bank,entry,data,successCallback,errorCallback){
        self.$http({
            method: 'POST',
            url: self.url+'/bank/'+bank+'/entry/'+entry,
            data:data
            }).then(function _successCallback(response) {
                console.log(response);
                successCallback(response.data.data);
            }, function _errorCallback(response) {
                console.log("Error",response);
                if (errorCallback!==undefined)
                    errorCallback(response);
            });
    }
}