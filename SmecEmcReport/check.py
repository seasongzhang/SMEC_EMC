class Chker:
    def __init__(self, prt_path):
        self.prt_path = prt_path
        self.txt_set = {'project.txt', 'parts.txt', 'actions.txt', 'steps.txt'}

    def txts_exist(self):
        try:
            # txt_list = os.listdir( os.path.join( self.prt_path, "txt" ) )
            txt_list = ['project.txt', 'parts.txt', 'actions.txt', 'teps.txt']
        except WindowsError:
            print("Error: directory 'txt' missing.")
            return False

        def print_txt_state(flist, state_str):
            for x in flist:
                print("file %s is " % x + state_str)

        if not self.txt_set == set( txt_list ):
            print_txt_state( self.txt_set - set( txt_list ), "missing." )
            print_txt_state( set( txt_list ) - self.txt_set, "useless." )
            return False


c = Chker( 'a' )
c.txts_exist( )
# def has_right_format(self):
#     if os.path.exists( os.path.join( self.dir_path, file_name ) ):
#         items = []
#         with codecs.open( os.path.join( self.dir_path, file_name ), encoding='utf-8' ) as f:
#             lines = [line for line in f.readlines( ) if (not line == "\r\n") and (not line == "\n")]
#             for (n, line) in enumerate( lines ):
#                 try:
#                     assert line.startswith( args[n % len( args )] )
#                 except AssertionError:
#                     print(n, len( args ), line)
#                     print("Wrong format of data in " + file_name + ", number " + str( (n % len( args )) + 1 ))
#                 else:
#                     items.append( line.split( ":" )[1].strip( ) )
#         items = [items[n:n + len( args )] for n in xrange( 0, len( items ), len( args ) )]
