# IMPORTS

# Reads and writes json
import json

# DEFAULTS


# The stats that a new user has
newUser = {
    "Eekros": 50,
    "exp": 0,
    "level": 0,
    "duid": None,
    "username": None
}

# Placeholder for EcoData; set by init()
data = None

# ERRORS


# An invalid user was passed, such as a user that does not exist.
class InvalidUserError(Exception):
    pass


# An invalid key was passed, such as a key that doesn't exist.
class InvalidKeyError(Exception):
    pass


# A username has already been taken.
class UsernameTakenError(Exception):
    pass


# Someone attempted to create more than one account.
class ExceededMaximumUsersError(Exception):
    pass

# FUCNTIONS


# Get the data from EcoData
async def getdata():
    with open("EcoData.json", "r") as ecoFile:
        return json.load(ecoFile)


# Write data to EcoData
async def writedata(dat):
    global data
    data["data"] = dat
    with open("EcoData.json", "w") as ecoFile:
        json.dump(data, ecoFile)


# Delete a key from EcoData.data
async def delkey(key):
    global data
    if key in data["data"]:
        del data["data"][key]
        writedata(data["data"])
    else:
        raise InvalidKeyError(f"The provided key ('{key}') is not in the data dict.")


# Creates a new user; duid stands for Discord User ID
async def writeuser(username, duid):
    global data
    if username not in data["data"]["users"] and not any([x["duid"] for key, x in data["data"]["users"].items()]):
        localnewuser = newUser
        localnewuser["duid"] = duid
        localnewuser["username"] = username
        data["data"]["users"][username] = localnewuser
        await writedata(data["data"])
    else:
        if username in data["data"]["users"]:
            raise UsernameTakenError("The username is already taken.")
        if any([x["duid"] for key, x in data["data"]["users"].items()]):
            raise ExceededMaximumUsersError("You've already created a user.")


# Deletes a user
async def deluser(username):
    global data
    if username in data["data"]["users"]:
        del data["data"]["users"][username]

        await writedata(data["data"])
    else:
        raise InvalidUserError(f"The provided username ('{username}') is not in the database")


# Writes a value to the user's dict
async def writeuserdat(username, key, value):
    global data
    if username in data["data"]["users"]:
        data["data"]["users"][username][key] = value
        await writedata(data["data"])
    else:
        raise InvalidUserError(f"The provided username ('{username}') is not in the database")


# Removes a value from the user's dict
async def deluserdat(username, key):
    global data
    if username in data["data"]["users"]:
        if key in data["data"]["users"][username]:
            del data["data"]["users"][username][key]
            await writedata(data["data"])
        else:
            raise InvalidKeyError(f"The provided key ('{key}') is not in the user's ({username}'s) dict.")
    else:
        raise InvalidUserError(f"The provided username ('{username}') is not in the database")


# Iniitialize
async def init():
    global data
    data = await getdata()
