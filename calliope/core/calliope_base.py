import os, inspect


class CalliopeBase(object):
    print_kwargs = ()

    # TO DO: CONSIDER... remove args here?
    def __init__(self, *args, **kwargs): 

        # TO DO: consider implementing set_... to auto-set properties based on class attributes

        for dub_attr in filter(lambda x: x[:4]=="dub_", dir(self)):
            print("YO MAMA", dub_attr)
            setattr(self, dub_attr[4:], getattr(self.__class__, dub_attr))

        for name, value in kwargs.items():
            setattr(self, name, value)

    def get_module_info(self):
        """Returns a tuple with the path and name for the module in which this bubble class is defined"""
        module_file = inspect.getmodule(self).__file__
        return os.path.dirname(module_file), os.path.split(module_file)[1].split(".")[0]

    def get_output_path(self, 
            directory=None, 
            sub_directory="illustrations", 
            filename=None, 
            filename_suffix="",
            **kwargs
            ):

        if not directory or not filename:
            module_directory, module_name = self.get_module_info()
        
        directory = directory or module_directory
        full_directory = os.path.join(directory, sub_directory)
        if not os.path.exists(full_directory):
            os.makedirs(full_directory)

        if not filename:
            filename = module_name
            my_name = getattr(self, "name", "")
            if my_name:
                filename = "_".join([filename, str.lower(my_name)])

        if filename_suffix:
            filename = "_".join([filename, filename_suffix])

        return os.path.join(full_directory, filename)

    def print_comments(self):
        """
        hook for adding 'comments' to end of __str__
        """
        return ""

    def __str__(self):
        # TO DO: add test for this!
        my_args = []
        my_name = getattr(self, "name", None)
        if  my_name: 
            my_args.append('"%s"' % my_name)
        for k in self.print_kwargs:
            v = getattr(self, k, None)
            v = '"%s"' % v if isinstance(v, str) else str(v)
            my_args.append(k + "=" + v)
        my_args_string = ", ".join(my_args)
        my_comments = self.print_comments()
        my_comments = " # " + my_comments if my_comments else ""
        return self.__module__ + "." + type(self).__name__ + "(" + my_args_string + ")" + my_comments

    # TO DO... reconcile this with __str__?
    def _feedback(self, msg_prefix, msg="(no message)", msg_data=None, **kwargs):
        print("%s - %s/%s: %s" % (msg_prefix, self.__class__.__name__, getattr(self, "name", "no name"), msg)  )
        if msg_data is not None:    
            print(msg_data)
        for name, value in kwargs.items():
            print(name + ": " + str(value) )
        print("------------------------------------------------------------")        

    def warn(self, *args, **kwargs):
        self._feedback("WARNING", *args, **kwargs)

    def info(self, *args, **kwargs):
        self._feedback("INFO", *args, **kwargs)

    def verify(self, condition, *args, **kwargs):
        if not condition:
            self.warn(*args, **kwargs)
        return condition