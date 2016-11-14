from resource_management import *

class HttpFS_service_check(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        Logger.info("Checking HttpFS service")
        #@TODO: find better check
        Execute(format("curl 'http://127.0.0.1:{params.httpfs_server_port}/webhdfs/v1/tmp/?op=liststatus&user.name={params.smoke_user}'"))
        Logger.info("Checking HttpFS service - DONE")

if __name__ == "__main__":
    HttpFS_service_check().execute()
