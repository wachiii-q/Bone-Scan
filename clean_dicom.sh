# Replace 'outer_folder' with the actual name of your outer folder
outer_folder="./data/Preliminary_BoneImage"
destination_folder="./data/temp" # << change the destination folder here

# # For ScreenCap files
# find "$outer_folder" -type d | while read main_folder; do
#   find "$main_folder" -type f -name "*ScreenCap*" | while read file; do
#     folder_name=$(dirname "$file")
#     new_file="${folder_name##*/}.dcm"
#     cp "$file" "$destination_folder/$new_file"
#   done
# done


# For AntPos files
find "$outer_folder" -type d | while read main_folder; do
  find "$main_folder" -type f \( -name "*ANT001*" -o -name "*ANTERIOR001*" \) | while read file; do
    folder_name=$(dirname "$file")
    new_file="${folder_name##*/}.dcm"
    cp "$file" "$destination_folder/$new_file"
  done
done