﻿using BLREdit.UI.Views;

using System;
using System.Resources;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace BLREdit.UI.Controls;

/// <summary>
/// Interaction logic for WeaponControl.xaml
/// </summary>
public sealed partial class WeaponControl : UserControl, INotifyPropertyChanged
{
    #region Events
    public event PropertyChangedEventHandler PropertyChanged;
    private void OnPropertyChanged([CallerMemberName] string propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
    #endregion Events

    private bool IsPrimary = true;

    private Visibility recieverVisibility = Visibility.Visible;
    public Visibility RecieverVisibility { get { return recieverVisibility; } private set { recieverVisibility = value; OnPropertyChanged(); } }

    private Visibility skinVisibility = Visibility.Collapsed;
    public Visibility SkinVisibility { get { return skinVisibility; } private set { skinVisibility = value; OnPropertyChanged(); } }



    private Visibility ammoVisibility = Visibility.Visible;
    public Visibility AmmoVisibility { get { return ammoVisibility; } private set { ammoVisibility = value; OnPropertyChanged(); } }

    private Visibility barrelVisibility = Visibility.Visible;
    public Visibility BarrelVisibility { get { return barrelVisibility; } private set { barrelVisibility = value; OnPropertyChanged(); } }

    private Visibility cammoVisibility = Visibility.Visible;
    public Visibility CamoVisibility { get { return cammoVisibility; } private set { cammoVisibility = value; OnPropertyChanged(); } }

    private Visibility tagVisibility = Visibility.Visible;
    public Visibility TagVisibility { get { return tagVisibility; } private set { tagVisibility = value; OnPropertyChanged(); } }

    private Visibility magazineVisibility = Visibility.Visible;
    public Visibility MagazineVisibility { get { return magazineVisibility; } private set { magazineVisibility = value; OnPropertyChanged(); } }

    private Visibility muzzleVisibility = Visibility.Visible;
    public Visibility MuzzleVisibility { get { return muzzleVisibility; } private set { muzzleVisibility = value; OnPropertyChanged(); } }

    private Visibility scopeVisibility = Visibility.Visible;
    public Visibility ScopeVisibility { get { return scopeVisibility; } private set { scopeVisibility = value; OnPropertyChanged(); } }

    private Visibility stockVisibility = Visibility.Visible;
    public Visibility StockVisibility { get { return stockVisibility; } private set { stockVisibility = value; OnPropertyChanged(); } }


    private Visibility gripVisibility = Visibility.Collapsed;
    public Visibility GripVisibility { get { return gripVisibility; } private set { gripVisibility = value; OnPropertyChanged(); } }


    public WeaponControl()
    {
        InitializeComponent();
        BLREditSettings.Settings.AdvancedModding.PropertyChanged += SettingsChanged;
        UIKeys.Keys[Key.LeftShift].PropertyChanged += SkinModifierChanged;
    }

    public void SkinModifierChanged(object sender, PropertyChangedEventArgs e)
    {
        if (IsPrimary)
        {
            if (UIKeys.Keys[Key.LeftShift].Is)
            {
                this.SkinVisibility = Visibility.Visible;
                this.RecieverVisibility = Visibility.Collapsed;
            }
            else
            {
                this.SkinVisibility = Visibility.Collapsed;
                this.RecieverVisibility = Visibility.Visible;
            }
        }
    }

    public void SettingsChanged(object sender, PropertyChangedEventArgs e)
    {
        Reciever_DataContextChanged(null, new DependencyPropertyChangedEventArgs());
    }

    private void UserControl_DataContextChanged(object sender, DependencyPropertyChangedEventArgs e)
    {
        ScopePreviewImage.DataContext = this.DataContext;
    }

    public static int PrimarySelectedBorder { get; private set; } = 6;
    public static int SecondarySelectedBorder { get; private set; } = -1;
    private void Grid_MouseUp(object sender, MouseButtonEventArgs e)
    {
        Border border = null;
        if (e.Source is Image image)
        {
            if (image.Parent is Border newBorder)
            {
                border = newBorder;
            }
        }
        if (e.Source is Border newBorder2)
        {
            border = newBorder2;
        }
        if (DataContext is BLRWeapon weapon)
        {
            if (weapon.IsPrimary)
            {
                PrimarySelectedBorder = this.ControlGrid.Children.IndexOf(border);
                SecondarySelectedBorder = -1;
            }
            else
            {
                SecondarySelectedBorder = this.ControlGrid.Children.IndexOf(border);
                PrimarySelectedBorder = -1;
            }
        }
    }

    internal void ApplyBorder()
    {
        if (DataContext is BLRWeapon weapon)
        {
            int index;

            if (weapon.IsPrimary)
            {
                index = PrimarySelectedBorder;
            }
            else
            {
                index = SecondarySelectedBorder;
            }

            if (index > -1 && index < this.ControlGrid.Children.Count && this.ControlGrid.Children[index] is Border border)
            {
                var mouse = new MouseButtonEventArgs(Mouse.PrimaryDevice, 0, MouseButton.Left);
                mouse.RoutedEvent = Mouse.MouseUpEvent;
                border.RaiseEvent(mouse);
            }
        }

    }

    private void Reciever_DataContextChanged(object sender, DependencyPropertyChangedEventArgs e)
    {
        if (DataContext is BLRWeapon weapon)
        {
            if (weapon.Reciever.SupportedMods.Contains("ammo") || BLREditSettings.Settings.AdvancedModding.Is)
            { AmmoVisibility = Visibility.Visible; }
            else
            { AmmoVisibility = Visibility.Collapsed; }

            if (weapon.Reciever.SupportedMods.Contains("barrels") || BLREditSettings.Settings.AdvancedModding.Is)
            { BarrelVisibility = Visibility.Visible; }
            else
            { BarrelVisibility = Visibility.Collapsed; }

            if (weapon.Reciever.SupportedMods.Contains("camosWeapon") || BLREditSettings.Settings.AdvancedModding.Is)
            { CamoVisibility = Visibility.Visible; }
            else
            { CamoVisibility = Visibility.Collapsed; }

            if (weapon.Reciever.SupportedMods.Contains("hangers") || BLREditSettings.Settings.AdvancedModding.Is)
            { TagVisibility = Visibility.Visible; }
            else
            { TagVisibility = Visibility.Collapsed; }

            if (weapon.Reciever.SupportedMods.Contains("magazines") || BLREditSettings.Settings.AdvancedModding.Is)
            { MagazineVisibility = Visibility.Visible; }
            else
            { MagazineVisibility = Visibility.Collapsed; }

            if (weapon.Reciever.SupportedMods.Contains("muzzles") || BLREditSettings.Settings.AdvancedModding.Is)
            { MuzzleVisibility = Visibility.Visible; }
            else
            { MuzzleVisibility = Visibility.Collapsed; }

            if (weapon.Reciever.SupportedMods.Contains("scopes") || BLREditSettings.Settings.AdvancedModding.Is)
            { ScopeVisibility = Visibility.Visible; }
            else
            { ScopeVisibility = Visibility.Collapsed; }

            if (weapon.Reciever.SupportedMods.Contains("stocks") || BLREditSettings.Settings.AdvancedModding.Is)
            { StockVisibility = Visibility.Visible; }
            else
            { StockVisibility = Visibility.Collapsed; }
        }
    }
}
