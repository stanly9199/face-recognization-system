from supabase import create_client, Client

# Replace these with your Supabase project details
url = "https://ldhkgewrbqvhipuvuuzy.supabase.co"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkaGtnZXdyYnF2aGlwdXZ1dXp5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNjQwODA3OSwiZXhwIjoyMDQxOTg0MDc5fQ.kPul3SBWekxBguHJXrDBCnnvgmsAOwBBrp7DPnFSZNs"

supabase: Client = create_client(url, api_key)

def str_to_list(str):
    return str.split(',')

def list_to_str(list):
    return ''.join(list)

def insert_result(name, img):
    response = supabase.table('record').insert([{
        "name": name,
        "image": img,
    }]).execute()
    
    # print(response)

def get_image():
    response = supabase.table('person').select('name').neq('permission', 'User').neq('permission', 'Blocked').execute()
    
    print(response)
    
    names: list = []
    
    for i in range(len(response.data)):
        names.append(response.data[i]['name'])

    print(names)
    
    images: list[tuple[str, list: str]] = []
    
    for name in names:
        res = supabase.table('recognition').select('image').eq('name', name).execute()
        for i in range(len(res.data)):
            imgs = res.data[i]['image']
            images.append((name, str_to_list(imgs)))
    print(images)
    
    return images

def get_admin():
    response = supabase.table('person').select('line_id').eq('permission', 'Admin').execute()
    # print(response)
    IDs: list = []
    for i in range(len(response.data)):
        IDs.append(response.data[i]['line_id'])
    # print(IDs)
    with open('admin_list.txt', 'w') as f:
        # write elements of list
        for id in IDs:
            f.write('%s\n' %id)
    with open('admin_list.txt') as f:
        admins = f.read().splitlines()
    # print(admins)
    return admins


if __name__ == '__main__':
    # insert_result()
    get_image()
    # get_admin()