from aocd import get_data
import os

input = get_data(day=7).splitlines()

#input = "$ cd /\n$ ls\ndir a\n14848514 b.txt\n8504156 c.dat\ndir d\n$ cd a\n$ ls\ndir e\n29116 f\n2557 g\n62596 h.lst\n$ cd e\n$ ls\n584 i\n$ cd ..\n$ cd ..\n$ cd d\n$ ls\n4060174 j\n8033020 d.log\n5626152 d.ext\n7214296 k"
#input = input.splitlines()

current_dir = ""
sizes = dict()

for line in input:
    if line == "$ cd /":
        current_dir = "/"
    elif line == "$ cd ..":
        current_dir = os.path.dirname(current_dir)
    elif line.startswith("$ cd"):
        current_dir = os.path.join(current_dir, line[5:])
    elif line == "$ ls":
        if current_dir not in sizes.keys():
            sizes[current_dir] = 0
    elif line.startswith("dir"):
        ## WHAT TO DO HERE?
        continue
    else:
        # Add size to the current directory
        filesize = int(line.split(" ")[0])
        #print(f"Found file {line.split(' ')[1]} of size {filesize} in dir {current_dir}")
        sizes[current_dir] += filesize

        # Also backtrack on the whole directory tree to add the size to the upper level directories
        temp = os.path.dirname(current_dir)
        while temp != "/":
            sizes[temp] += filesize
            temp = os.path.dirname(temp)

        # When temp == "/" we still need to add the file size to the highest level dir
        # (But only if we were not already on the highest level dir)
        if current_dir != "/":
            sizes[temp] += filesize

print(sizes)

# Question 1
small_folder_size_sum = sum([size for size in sizes.values() if size <= 100000])
print(small_folder_size_sum)

# Question 2
total_free_space = 70000000 - sizes["/"]
needed_extra_space = 30000000 - total_free_space
potential_dirs_to_delete = {dirname:size for dirname, size in sizes.items() if size >= needed_extra_space}
print("Size of directory to delete:", min(potential_dirs_to_delete.values()))
