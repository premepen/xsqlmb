class LocalUtil():
    @staticmethod
    def get_uniq_date_str():
        from datetime import datetime
        return str(datetime.now().date())


class NginxLogDestination(object):
    def send(self, msg):
        self.outfile = open("/opt/log/nginx.txt" + "-" + LocalUtil.get_uniq_date_str() , "a")
        for key,v in msg.items():
            self.outfile.write(str(key) + "=" + str(v) + "\n");
            self.outfile.write("==========================\n" )
            self.outfile.write( str(v) )
            self.outfile.write("======================================\n" )

        self.outfile.flush()
        self.outfile.close()
        return True