using ExampleMod.Dusts;
using Microsoft.Xna.Framework;
using Terraria;
using Terraria.ID;
using Terraria.ModLoader;

namespace ChangeThisToModName
{
    public class ZenithOre : ModTile
    {
        public override void SetStaticDefaults()
        {
            Main.tileSolid[Type] = true; // will work on this later
            Main.tileMergeDirt[Type] = false; // will work on this later
            Main.tileBlockLight[Type] = false; // will work on this later
            Main.tileLighted[Type] = true; // will work on this later
            DustType = DustID.Obsidian;
            AddMapEntry(new Color(200, 200, 200)); // will work on this later

            MineResist = 5f;
            MinPick = 210;
        }
    }
}