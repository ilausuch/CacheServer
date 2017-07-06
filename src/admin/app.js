var app = angular.module('app', ['il.ui.modal','il.ui.input']);
var mc;


app.controller("MainController", function($scope,$timeout,$http,$q){
    mc=this;
    this.$http=$http;
    this.$timeout=$timeout;
    
    this.menu="connection";
    this.url="http://"+location.host.split(":")[0]+":5000";
    
    
    this.goToMenu=function(id){
        this.menu=id;
        switch(this.menu){
            case "cache":
                this.submenu="banks";
            break;
            default:
                this.submenu="";
        
        }
    };
    
    this.goToSubMenu=function(id){
        this.submenu=id;
    };
    
    this.connect=function(){
        this.connection=new CacheClient(this.url,$http);
        
        this.connecting=true;
        this.errorConnecting=false;
        
        this.connection.getBanks(function(data){
            mc.connected=true;
            mc.connecting=false;
            mc.goToMenu("cache");
            mc.banks=data;
        },function(err){
            mc.disconnect();
            mc.errorConnecting=true;
        });
    };
    
    this.disconnect=function(){
        this.connecting=false;
        this.connection=undefined;
        this.connected=false;
        this.selectedBank=undefined;
        this.selectedEntry=undefined;
    };
    
    this.selectBank=function(bank){
        this.selectedBank=bank;
        this.selectedEntry=undefined;
        this.entryData=undefined;
        this.bankEntries=undefined;
        
        this.connection.getElements(mc.selectedBank,function(data){
            mc.bankEntries=data;
        });
    };
    
    this.selectEntry=function(entry){
        this.selectedEntry=entry;
        this.entryValue=undefined;
        this.connection.getValue(mc.selectedBank,mc.selectedEntry,function(data){
            mc.entryValue=data;
            mc.edit.editEntryValue(mc.selectedBank,mc.selectedEntry,mc.entryValue,function(){
                mc.selectedEntry=undefined;
                mc.entryValue=undefined;
            });
        });
    };
    
    this.addEntry=function(){
        mc.edit.editEntry(mc.selectedBank,"","",function(){
            mc.selectBank(mc.selectedBank);
        });
    };
    
    this.addBank=function(){
        mc.edit.editAll("","","",function(){
            mc.connect();
        });
    };
    
    this.edit={
        show:false,
        showSaved:false,
        
        
        _edit:function(bank,key,value,callback){
            this.bank=bank;
            this.key=key;
            this.value=value;
            
            this.show=true;
            this.showBank=false;
            this.showKey=false;
            
            this.callback=callback;
        },
        editEntryValue:function(bank,key,value,callback){
            this._edit(bank,key,value,callback);
        },
        
        editEntry:function(bank,key,value,callback){
            this._edit(bank,key,value,callback);
            this.showKey=true;
        },
        
        editAll:function(bank,key,value,callback){
            this._edit(bank,key,value,callback);
            this.showBank=true;
            this.showKey=true;
        },
        
        save:function(){
            var $this=this;
            
            mc.connection.setValue(this.bank,this.key,this.value,function(data){
                $this.show=false;
                $this.showSaved=true;
                mc.$timeout(function(){
                    $this.showSaved=false;
                },1000);
                
                $this.callback();
            });
        }
        
    };
    
    
});
