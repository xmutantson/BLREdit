﻿using BLREdit.Import;

using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace BLREdit.UI.Windows;

/// <summary>
/// Interaction logic for MapModeSelect.xaml
/// </summary>
public sealed partial class MapModeSelect : Window
{
    public static List<BLRMap> Maps { get; } = IOResources.DeserializeFile<List<BLRMap>>("Assets\\json\\maps.json");
    public static List<BLRMode> Modes { get; } = IOResources.DeserializeFile<List<BLRMode>>("Assets\\json\\modes.json");

    private BLRMap SelectedMap = null;
    private BLRMode SelectedMode = null;
    private bool CanClose = true;

    static MapModeSelect()
    {
        foreach (var map in Maps)
        {
            foreach (var mode in Modes)
            {
                if (map.SupportedPlaylists.Contains(mode.PlaylistName))
                {
                    map.SupportedGameModes.Add(mode);
                    
                }
            }
            LoggingSystem.Log($"{map.MapName} GameModes:({map.SupportedGameModes.Count}/{map.SupportedPlaylists.Count})");
        }
    }

    public MapModeSelect(string clientVersion)
    {
        InitializeComponent();
        this.MapList.Items.Filter += new Predicate<object>(o =>
        {
            if (clientVersion == "Unknown") { return true; }
            if (o is BLRMap map)
            {
                return map.Available.Contains(clientVersion);
            }
            return false;
        });
    }

    public static (BLRMode Mode, BLRMap Map) SelectMapAndMode(string clientVersion)
    {
        MapModeSelect window = new(clientVersion);
        window.ShowDialog();
        return (window.SelectedMode, window.SelectedMap);
    }

    private void WindowLoaded(object sender, RoutedEventArgs e)
    {
        this.MapList.ItemsSource = Maps;
    }

    private void Button_Click(object sender, RoutedEventArgs e)
    {
        var button = (Button)e.Source;
        var grid = (Grid)button.Parent;
        var comboBox = (ComboBox)grid.Children[2];
        SelectedMode = (BLRMode)comboBox.SelectedItem;
        SelectedMap = (BLRMap)button.DataContext;
        CanClose = false;
        this.Close();
    }

    private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
    {
        e.Cancel = CanClose;
    }
}
